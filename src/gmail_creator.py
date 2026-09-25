"""
Gmail Bulk Creator - Main business logic
"""

import csv
import time
import logging
from typing import List, Dict, Any
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from src.config import Config

class GmailBulkCreator:
    """Main class for creating Gmail accounts in bulk"""
    
    GMAIL_SIGNUP_URL = "https://accounts.google.com/signup/v2/webcreateaccount"
    
    def __init__(self, config: Config, logger: logging.Logger):
        """
        Initialize Gmail Bulk Creator
        
        Args:
            config: Configuration object
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.driver = None
        self.wait = None
    
    def setup_driver(self) -> webdriver.Chrome:
        """Setup Selenium WebDriver"""
        try:
            options = webdriver.ChromeOptions()
            
            if self.config.headless_mode:
                options.add_argument('--headless')
            
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Add proxy if configured
            proxy = self.config.get_proxy()
            if proxy:
                options.add_argument(f'--proxy-server={proxy}')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.implicitly_wait(self.config.implicit_wait)
            
            self.logger.info("WebDriver initialized successfully")
            return driver
        
        except Exception as e:
            self.logger.error(f"Failed to setup WebDriver: {str(e)}")
            raise
    
    def load_accounts_from_csv(self, csv_file: str) -> List[Dict[str, str]]:
        """
        Load account data from CSV file
        
        Args:
            csv_file: Path to CSV file with account data
        
        Returns:
            List of account dictionaries
        """
        accounts = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                accounts = list(reader)
            
            self.logger.info(f"Loaded {len(accounts)} accounts from {csv_file}")
            return accounts
        
        except FileNotFoundError:
            self.logger.warning(f"File not found: {csv_file}")
            return []
        except Exception as e:
            self.logger.error(f"Error reading CSV: {str(e)}")
            return []
    
    def create_gmail_account(self, account_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Create a single Gmail account
        
        Args:
            account_data: Dictionary with account information
                Expected keys: first_name, last_name, email, password, recovery_email, birth_date, gender
        
        Returns:
            Result dictionary with status and details
        """
        result = {
            'email': account_data.get('email'),
            'status': 'pending',
            'message': '',
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            if not self.driver:
                self.driver = self.setup_driver()
                self.wait = WebDriverWait(self.driver, 15)
            
            self.logger.info(f"Creating account: {account_data.get('email')}")
            
            # Navigate to Gmail signup
            self.driver.get(self.GMAIL_SIGNUP_URL)
            time.sleep(2)
            
            # Fill in first name
            first_name_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "firstName"))
            )
            first_name_field.clear()
            first_name_field.send_keys(account_data.get('first_name', ''))
            
            # Fill in last name
            last_name_field = self.driver.find_element(By.ID, "lastName")
            last_name_field.clear()
            last_name_field.send_keys(account_data.get('last_name', ''))
            
            # Click next
            next_button = self.driver.find_element(By.ID, "identifierNext")
            next_button.click()
            time.sleep(2)
            
            # Fill in email
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.clear()
            email_field.send_keys(account_data.get('email', ''))
            
            # Click next
            next_button = self.driver.find_element(By.ID, "identifierNext")
            next_button.click()
            time.sleep(2)
            
            # Fill in password
            password_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_field.clear()
            password_field.send_keys(account_data.get('password', ''))
            
            # Fill in confirm password
            confirm_password_field = self.driver.find_element(By.NAME, "confirm_password")
            confirm_password_field.clear()
            confirm_password_field.send_keys(account_data.get('password', ''))
            
            # Click next
            next_button = self.driver.find_element(By.ID, "passwordNext")
            next_button.click()
            time.sleep(3)
            
            result['status'] = 'success'
            result['message'] = 'Account created successfully'
            self.logger.info(f"✓ Account created: {account_data.get('email')}")
        
        except Exception as e:
            result['status'] = 'failed'
            result['message'] = str(e)
            self.logger.error(f"✗ Failed to create account {account_data.get('email')}: {str(e)}")
        
        return result
    
    def create_accounts_bulk(self, accounts: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Create multiple Gmail accounts with batch processing
        
        Args:
            accounts: List of account dictionaries
        
        Returns:
            List of result dictionaries
        """
        results = []
        
        try:
            for idx, account in enumerate(accounts, 1):
                self.logger.info(f"Processing account {idx}/{len(accounts)}")
                
                result = self.create_gmail_account(account)
                results.append(result)
                
                # Delay between accounts
                if idx < len(accounts):
                    time.sleep(self.config.delay_between_accounts)
        
        except KeyboardInterrupt:
            self.logger.warning("Process interrupted by user")
        
        finally:
            self.close_driver()
        
        return results
    
    def save_results(self, results: List[Dict[str, Any]], output_file: str) -> None:
        """
        Save results to CSV file
        
        Args:
            results: List of result dictionaries
            output_file: Path to output CSV file
        """
        try:
            if not results:
                self.logger.warning("No results to save")
                return
            
            # Create output directory if it doesn't exist
            import os
            os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
            
            self.logger.info(f"Results saved to {output_file}")
        
        except Exception as e:
            self.logger.error(f"Error saving results: {str(e)}")
    
    def close_driver(self) -> None:
        """Close the WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver closed")
            except Exception as e:
                self.logger.error(f"Error closing WebDriver: {str(e)}")
    
    def __del__(self):
        """Destructor to ensure WebDriver is closed"""
        self.close_driver()
