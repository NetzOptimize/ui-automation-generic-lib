import requests
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import time

"""
Todo:
    explicit wait all options
    count
    drag to
    highlight
    nth
    screenshot
    wait for 
    scroll into view
    select text
    copy to clipboard
    find_element(By.ID, "id")
find_element(By.NAME, "name")
find_element(By.XPATH, "xpath") - done 
find_element(By.LINK_TEXT, "link text")
find_element(By.PARTIAL_LINK_TEXT, "partial link text")
find_element(By.TAG_NAME, "tag name")
find_element(By.CLASS_NAME, "class name")
find_element(By.CSS_SELECTOR, "css selector") - done

drag and drop 
element = driver.find_element(By.NAME, "source")
target = driver.find_element(By.NAME, "target")

from selenium.webdriver import ActionChains
action_chains = ActionChains(driver)
action_chains.drag_and_drop(element, target).perform()


history 
driver.forward()
driver.back()
"""
#################
# Types
#################

T_INPUT = 'input'
T_BUTTON = 'button'
T_CHECKBOX = 'checkbox'
T_DROPDOWN = 'dropdown'
T_RETURN = "return"

#################
# LOCATORS
#################

L_CSS = 'css'
L_XPATH = 'xpath'
L_NAME = 'name'
L_LINK_TEXT = 'link_text'
L_PARTIAL_LINK_TEXT = 'partial_link_text'
L_TAG_NAME = 'tag_name'
L_CLASS_NAME = 'class_name'

#################
# ACTIONS
#################

A_CLICK = 'click'
A_TYPE = 'type'
A_TEXT = 'text'
A_HOVER = 'hover'
A_HOVER_CLICK = 'hover_click'
A_VALUE = 'value'
A_INDEX = 'index'
A_VISIBLE = 'visible'

#################
# EXPLICIT WAIT TYPES
#################

E_CLICKABLE = "element_to_be_clickable"


#################
# ERRORS
#################

class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def as_string(self):
        results = f'{self.error_name}: {self.details} '
        return results


class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)


class NoSuchElementPresent(Error):
    def __init__(self, details):
        super().__init__('No such element', details)


# TODO: Function to make browser maximized
class Checker:
    """
    Base class for all checkers.
    """

    def __init__(self, url, driver):
        """
            Initialize the checker class

            Parameters
            ----------

            :param str url: input the url of the website
            :param driver: input the browser driverManager

        """
        self.filename = None
        self.ac_value2 = None
        self.time = None
        self.i = None
        self.func = None
        self.divpath = None
        self.m = None
        self.obj = None
        self.word = None
        self.ac2 = None
        self.lv2 = None
        self.locator2 = None
        self.ac_value = None
        self.lv = None
        self.locator = None
        self.ac = None
        self.tp = None
        self.url = url
        self.driver = driver
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        affirmative_url = self.valid_url(self.url)
        self.driver.get(f"{affirmative_url}")
        self.a = ActionChains(self.driver)

    def valid_url(self, url):
        try:
            req = requests.get(url)
            while req.status_code != requests.codes['ok']:
                assert False, f"Please enter a valid URL... {self.url} is not a valid URL."
        except Exception as ex:
            print(f'Something went wrong: {ex}')
            print('Try again!')
            assert False, f"Please enter a valid URL... {self.url} is not a valid URL."

        return url

    # TODO: check the functionality
    # working
    def display_url(self):
        """
                :return: Prints the url of the main url sent to the webdriver.
                :rtype: str
        """
        return print(f'Url is: {self.url}')

    # working
    def return_url(self):
        """
                :return: Returns the url of the main url sent to the webdriver.
                :rtype: str
        """
        return self.url

    # working
    def current_tab_url(self):
        """
                        :return: Returns the url of the current website in the current selected tab
                        :rtype: str
                """
        return self.driver.current_url

    # working
    def input(self, locator, locator_value, ac, ac_value):
        """
            Takes value from user and inputs in the field specified

            Parameters
            ----------


            :param str locator: xpath/css
            :param str locator_value: input the value of the locator as xpath of css selector
            :param str ac: action to be performed e.g. 'type'
            :param str ac_value: value for the action

        """
        self.locator = locator
        self.lv = locator_value
        self.ac = ac
        self.ac_value = ac_value
        if self.locator == L_CSS:
            if self.ac == A_TYPE:
                try:
                    self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}").send_keys(f"{self.ac_value}")
                except NoSuchElementException:
                    error = NoSuchElementPresent(
                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_XPATH:
            if self.ac == A_TYPE:
                try:
                    self.driver.find_element(By.XPATH, f"{self.lv}").send_keys(f"{self.ac_value}")
                except NoSuchElementException:
                    error = NoSuchElementPresent(
                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_NAME:
            if self.ac == A_TYPE:
                try:
                    self.driver.find_element(By.NAME, f"{self.lv}").send_keys(f"{self.ac_value}")
                except NoSuchElementException:
                    error = NoSuchElementPresent(
                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_LINK_TEXT:
            if self.ac == A_TYPE:
                try:
                    self.driver.find_element(By.LINK_TEXT, f"{self.lv}").send_keys(f"{self.ac_value}")
                except NoSuchElementException:
                    error = NoSuchElementPresent(
                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_PARTIAL_LINK_TEXT:
            if self.ac == A_TYPE:
                try:
                    self.driver.find_element(By.PARTIAL_LINK_TEXT, f"{self.lv}").send_keys(f"{self.ac_value}")
                except NoSuchElementException:
                    error = NoSuchElementPresent(
                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_TAG_NAME:
            if self.ac == A_TYPE:
                try:
                    self.driver.find_element(By.TAG_NAME, f"{self.lv}").send_keys(f"{self.ac_value}")
                except NoSuchElementException:
                    error = NoSuchElementPresent(
                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_CLASS_NAME:
            if self.ac == A_TYPE:
                try:
                    self.driver.find_element(By.CLASS_NAME, f"{self.lv}").send_keys(f"{self.ac_value}")
                except NoSuchElementException:
                    error = NoSuchElementPresent(
                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

    # working
    def button(self, locator, locator_value, ac):
        """
            Clicks a button

            Parameters
            ----------


            :param str locator: xpath/css
            :param str locator_value: input the value of the locator as xpath of css selector
            :param str ac: action to be performed e.g. 'click', or 'hover'

        """
        self.locator = locator
        self.lv = locator_value
        self.ac = ac
        if self.locator == L_CSS:
            if self.ac == A_CLICK:
                try:
                    self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}").click()
                    self.driver.implicitly_wait(10)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_XPATH:
            if self.ac == A_CLICK:
                try:
                    self.driver.find_element(By.XPATH, f"{self.lv}").click()
                    self.driver.implicitly_wait(10)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_NAME:
            if self.ac == A_CLICK:
                try:
                    self.driver.find_element(By.NAME, f"{self.lv}").click()
                    self.driver.implicitly_wait(10)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_LINK_TEXT:
            if self.ac == A_CLICK:
                try:
                    self.driver.find_element(By.LINK_TEXT, f"{self.lv}").click()
                    self.driver.implicitly_wait(10)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_PARTIAL_LINK_TEXT:
            if self.ac == A_CLICK:
                try:
                    self.driver.find_element(By.PARTIAL_LINK_TEXT, f"{self.lv}").click()
                    self.driver.implicitly_wait(10)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_TAG_NAME:
            if self.ac == A_CLICK:
                try:
                    self.driver.find_element(By.TAG_NAME, f"{self.lv}").click()
                    self.driver.implicitly_wait(10)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_CLASS_NAME:
            if self.ac == A_CLICK:
                try:
                    self.driver.find_element(By.CLASS_NAME, f"{self.lv}").click()
                    self.driver.implicitly_wait(10)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

    # working
    def static_dropdown(self, locator, locator_value, ac, ac_value):
        """
            Static dropdown -> Works with Select Tag

            Parameters
            ----------

            :param str locator: xpath/css
            :param str locator_value: input the value of the locator as xpath of css selector
            :param str ac: action to be performed e.g. 'value','visible' or 'index'
            :param str ac_value: value for the action

        """
        self.locator = locator
        self.lv = locator_value
        self.ac = ac
        self.ac_value = ac_value
        if self.locator == L_CSS:
            if self.ac == A_VALUE:
                try:
                    s_dropdown = Select(self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}"))
                    s_dropdown.select_by_value(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.ac == A_INDEX:
                try:
                    s_dropdown = Select(self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}"))
                    int(self.ac_value)
                    s_dropdown.select_by_index(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.ac == A_VISIBLE:
                try:
                    s_dropdown = Select(self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}"))
                    s_dropdown.select_by_visible_text(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_XPATH:
            if self.ac == A_VALUE:
                try:
                    s_dropdown = Select(self.driver.find_element(By.XPATH, f"{self.lv}"))
                    s_dropdown.select_by_value(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.ac == A_INDEX:
                try:
                    s_dropdown = Select(self.driver.find_element(By.XPATH, f"{self.lv}"))
                    int(self.ac_value)
                    s_dropdown.select_by_index(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.ac == A_VISIBLE:
                try:
                    s_dropdown = Select(self.driver.find_element(By.XPATH, f"{self.lv}"))
                    s_dropdown.select_by_visible_text(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_NAME:
            if self.ac == A_VALUE:
                try:
                    s_dropdown = Select(self.driver.find_element(By.NAME, f"{self.lv}"))
                    s_dropdown.select_by_value(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.ac == A_INDEX:
                try:
                    s_dropdown = Select(self.driver.find_element(By.NAME, f"{self.lv}"))
                    int(self.ac_value)
                    s_dropdown.select_by_index(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.ac == A_VISIBLE:
                try:
                    s_dropdown = Select(self.driver.find_element(By.NAME, f"{self.lv}"))
                    s_dropdown.select_by_visible_text(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_LINK_TEXT:
            if self.ac == A_VALUE:
                try:
                    s_dropdown = Select(self.driver.find_element(By.LINK_TEXT, f"{self.lv}"))
                    s_dropdown.select_by_value(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.ac == A_INDEX:
                try:
                    s_dropdown = Select(self.driver.find_element(By.LINK_TEXT, f"{self.lv}"))
                    int(self.ac_value)
                    s_dropdown.select_by_index(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.ac == A_VISIBLE:
                try:
                    s_dropdown = Select(self.driver.find_element(By.LINK_TEXT, f"{self.lv}"))
                    s_dropdown.select_by_visible_text(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_PARTIAL_LINK_TEXT:
            if self.ac == A_VALUE:
                try:
                    s_dropdown = Select(self.driver.find_element(By.PARTIAL_LINK_TEXT, f"{self.lv}"))
                    s_dropdown.select_by_value(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.ac == A_INDEX:
                try:
                    s_dropdown = Select(self.driver.find_element(By.PARTIAL_LINK_TEXT, f"{self.lv}"))
                    int(self.ac_value)
                    s_dropdown.select_by_index(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.ac == A_VISIBLE:
                try:
                    s_dropdown = Select(self.driver.find_element(By.PARTIAL_LINK_TEXT, f"{self.lv}"))
                    s_dropdown.select_by_visible_text(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_TAG_NAME:
            if self.ac == A_VALUE:
                try:
                    s_dropdown = Select(self.driver.find_element(By.TAG_NAME, f"{self.lv}"))
                    s_dropdown.select_by_value(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.ac == A_INDEX:
                try:
                    s_dropdown = Select(self.driver.find_element(By.TAG_NAME, f"{self.lv}"))
                    int(self.ac_value)
                    s_dropdown.select_by_index(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.ac == A_VISIBLE:
                try:
                    s_dropdown = Select(self.driver.find_element(By.TAG_NAME, f"{self.lv}"))
                    s_dropdown.select_by_visible_text(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_CLASS_NAME:
            if self.ac == A_VALUE:
                try:
                    s_dropdown = Select(self.driver.find_element(By.CLASS_NAME, f"{self.lv}"))
                    s_dropdown.select_by_value(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.ac == A_INDEX:
                try:
                    s_dropdown = Select(self.driver.find_element(By.CLASS_NAME, f"{self.lv}"))
                    int(self.ac_value)
                    s_dropdown.select_by_index(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.ac == A_VISIBLE:
                try:
                    s_dropdown = Select(self.driver.find_element(By.CLASS_NAME, f"{self.lv}"))
                    s_dropdown.select_by_visible_text(self.ac_value)
                except NoSuchElementException:
                    error = NoSuchElementPresent(f"{self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

    # working
    def dynamic_dropdown(self, tp, locator, locator_value, ac, ac_value, locator2, locator_value2, ac2, ac_value2):
        """


            Parameters
            ----------

            :param str tp: Type of input e.g. 'input'
            :param str locator: xpath/css
            :param str locator_value: input the value of the locator as xpath of css selector
            :param str ac: action to be performed e.g. 'type'
            :param str ac_value: value for the action
            :param str locator2: xpath/css
            :param str locator_value2: input the value of the locator as xpath of css selector
            :param str ac2: action to be performed e.g. 'type'
            :param str ac_value2: value for the action

        """
        self.tp = tp
        self.locator = locator
        self.lv = locator_value
        self.ac = ac
        self.ac_value = ac_value
        self.locator2 = locator2
        self.lv2 = locator_value2
        self.ac2 = ac2
        self.ac_value2 = ac_value2
        if self.tp == T_INPUT:
            if self.locator == L_CSS:
                if self.ac == A_TYPE:
                    try:
                        self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}").send_keys(f"{self.ac_value}")
                        if self.locator2 == L_CSS:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_XPATH:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.XPATH, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.XPATH, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_LINK_TEXT:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.LINK_TEXT, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.LINK_TEXT, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_PARTIAL_LINK_TEXT:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.PARTIAL_LINK_TEXT, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.PARTIAL_LINK_TEXT, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_TAG_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.TAG_NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.TAG_NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_CLASS_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CLASS_NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CLASS_NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        else:
                            error = IllegalCharError(f"{self.locator2}")
                            print(error.as_string())
                            assert False, f"{error.as_string()}"
                    except NoSuchElementException:
                        error = NoSuchElementPresent(
                            f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                        print(error.as_string())
                        assert False, f"{error.as_string()}"
                else:
                    error = IllegalCharError(f"{self.ac}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.locator == L_XPATH:
                if self.ac == A_TYPE:
                    try:
                        self.driver.find_element(By.XPATH, f"{self.lv}").send_keys(f"{self.ac_value}")
                        if self.locator2 == L_CSS:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_XPATH:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.XPATH, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.XPATH, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_LINK_TEXT:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.LINK_TEXT, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.LINK_TEXT, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_PARTIAL_LINK_TEXT:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.PARTIAL_LINK_TEXT, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.PARTIAL_LINK_TEXT, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_TAG_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.TAG_NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.TAG_NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_CLASS_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CLASS_NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CLASS_NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        else:
                            error = IllegalCharError(f"{self.locator2}")
                            print(error.as_string())
                            assert False, f"{error.as_string()}"
                    except NoSuchElementException:
                        error = NoSuchElementPresent(
                            f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                        print(error.as_string())
                        assert False, f"{error.as_string()}"
                else:
                    error = IllegalCharError(f"{self.ac}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.locator == L_NAME:
                if self.ac == A_TYPE:
                    try:
                        self.driver.find_element(By.NAME, f"{self.lv}").send_keys(f"{self.ac_value}")
                        if self.locator2 == L_CSS:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_XPATH:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.XPATH, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.XPATH, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_LINK_TEXT:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.LINK_TEXT, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.LINK_TEXT, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_PARTIAL_LINK_TEXT:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.PARTIAL_LINK_TEXT, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.PARTIAL_LINK_TEXT, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_TAG_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.TAG_NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.TAG_NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_CLASS_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CLASS_NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CLASS_NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        else:
                            error = IllegalCharError(f"{self.locator2}")
                            print(error.as_string())
                            assert False, f"{error.as_string()}"
                    except NoSuchElementException:
                        error = NoSuchElementPresent(
                            f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                        print(error.as_string())
                        assert False, f"{error.as_string()}"
                else:
                    error = IllegalCharError(f"{self.ac}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.locator == L_LINK_TEXT:
                if self.ac == A_TYPE:
                    try:
                        self.driver.find_element(By.LINK_TEXT, f"{self.lv}").send_keys(f"{self.ac_value}")
                        if self.locator2 == L_CSS:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_XPATH:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.XPATH, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.XPATH, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_LINK_TEXT:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.LINK_TEXT, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.LINK_TEXT, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_PARTIAL_LINK_TEXT:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.PARTIAL_LINK_TEXT, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.PARTIAL_LINK_TEXT, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_TAG_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.TAG_NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.TAG_NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_CLASS_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CLASS_NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CLASS_NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        else:
                            error = IllegalCharError(f"{self.locator2}")
                            print(error.as_string())
                            assert False, f"{error.as_string()}"
                    except NoSuchElementException:
                        error = NoSuchElementPresent(
                            f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                        print(error.as_string())
                        assert False, f"{error.as_string()}"
                else:
                    error = IllegalCharError(f"{self.ac}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.locator == L_PARTIAL_LINK_TEXT:
                if self.ac == A_TYPE:
                    try:
                        self.driver.find_element(By.PARTIAL_LINK_TEXT, f"{self.lv}").send_keys(f"{self.ac_value}")
                        if self.locator2 == L_CSS:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_XPATH:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.XPATH, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.XPATH, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_LINK_TEXT:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.LINK_TEXT, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.LINK_TEXT, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_PARTIAL_LINK_TEXT:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.PARTIAL_LINK_TEXT, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.PARTIAL_LINK_TEXT, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_TAG_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.TAG_NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.TAG_NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_CLASS_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CLASS_NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CLASS_NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        else:
                            error = IllegalCharError(f"{self.locator2}")
                            print(error.as_string())
                            assert False, f"{error.as_string()}"
                    except NoSuchElementException:
                        error = NoSuchElementPresent(
                            f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                        print(error.as_string())
                        assert False, f"{error.as_string()}"
                else:
                    error = IllegalCharError(f"{self.ac}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.locator == L_TAG_NAME:
                if self.ac == A_TYPE:
                    try:
                        self.driver.find_element(By.TAG_NAME, f"{self.lv}").send_keys(f"{self.ac_value}")
                        if self.locator2 == L_CSS:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_XPATH:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.XPATH, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.XPATH, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_LINK_TEXT:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.LINK_TEXT, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.LINK_TEXT, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_PARTIAL_LINK_TEXT:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.PARTIAL_LINK_TEXT, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.PARTIAL_LINK_TEXT, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_TAG_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.TAG_NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.TAG_NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_CLASS_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CLASS_NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CLASS_NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        else:
                            error = IllegalCharError(f"{self.locator2}")
                            print(error.as_string())
                            assert False, f"{error.as_string()}"
                    except NoSuchElementException:
                        error = NoSuchElementPresent(
                            f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                        print(error.as_string())
                        assert False, f"{error.as_string()}"
                else:
                    error = IllegalCharError(f"{self.ac}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            elif self.locator == L_CLASS_NAME:
                if self.ac == A_TYPE:
                    try:
                        self.driver.find_element(By.CLASS_NAME, f"{self.lv}").send_keys(f"{self.ac_value}")
                        if self.locator2 == L_CSS:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_XPATH:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.XPATH, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.XPATH, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_LINK_TEXT:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.LINK_TEXT, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.LINK_TEXT, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_PARTIAL_LINK_TEXT:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.PARTIAL_LINK_TEXT, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.PARTIAL_LINK_TEXT, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_TAG_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.TAG_NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.TAG_NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        elif self.locator2 == L_CLASS_NAME:
                            if self.ac2 == A_VALUE:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CLASS_NAME, f"{self.lv2}")
                                    time.sleep(2)
                                    for dropdown in d_dropdown:
                                        try:
                                            if dropdown.text == f"{self.ac_value2}":
                                                dropdown.click()
                                        except StaleElementReferenceException:
                                            print("element is not attached to the page document")
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            elif self.ac2 == A_INDEX:
                                try:
                                    d_dropdown = self.driver.find_elements(By.CLASS_NAME, f"{self.lv2}")
                                    index = int(self.ac_value2)
                                    index -= 1
                                    d_dropdown[index].click()
                                except NoSuchElementException:
                                    error = NoSuchElementPresent(
                                        f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value} -> {self.locator2} -> {self.lv2} -> {self.ac2} -> {self.ac_value2}")
                                    print(error.as_string())
                                    assert False, f"{error.as_string()}"
                            else:
                                error = IllegalCharError(f"{self.ac2}")
                                print(error.as_string())
                                assert False, f"{error.as_string()}"
                        else:
                            error = IllegalCharError(f"{self.locator2}")
                            print(error.as_string())
                            assert False, f"{error.as_string()}"
                    except NoSuchElementException:
                        error = NoSuchElementPresent(
                            f"{self.tp} -> {self.locator} -> {self.lv} -> {self.ac} -> {self.ac_value}")
                        print(error.as_string())
                        assert False, f"{error.as_string()}"
                else:
                    error = IllegalCharError(f"{self.ac}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.locator}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        else:
            error = IllegalCharError(f"{self.tp}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

    # working
    def slowmo(self, t):
        """
                    Slows the browser automation.
                    Parameters
                    ----------
                    :param float t: Time to wait (in seconds)

                 """
        self.time = t
        time.sleep(self.time)

    # working
    def popup_accept(self):
        try:
            WebDriverWait(self.driver, 3).until(ec.alert_is_present(),
                                                'Timed out waiting for PA creation ' +
                                                'confirmation popup to appear.')
            alert = self.driver.switch_to.alert
            alert.accept()
        except TimeoutException as ex:
            print(f'Something went wrong: {ex}')
            print('No alert present!')
            assert False, f"No alert present!"

    # working
    def popup_decline(self):
        try:
            WebDriverWait(self.driver, 3).until(ec.alert_is_present(),
                                                'Timed out waiting for PA creation ' +
                                                'confirmation popup to appear.')
            alert = self.driver.switch_to.alert
            alert.dismiss()
        except TimeoutException as ex:
            print(f'Something went wrong: {ex}')
            print('No alert present!')
            assert False, f"No alert present!"

    # working
    def popup_text(self):
        try:
            WebDriverWait(self.driver, 3).until(ec.alert_is_present(),
                                                'Timed out waiting for PA creation ' +
                                                'confirmation popup to appear.')
            alert = self.driver.switch_to.alert
            return alert.text
        except TimeoutException as ex:
            print(f'Something went wrong: {ex}')
            print('No alert present!')
            assert False, f"No alert present!"

    # working
    def file_upload(self, locator, locator_value, filename):
        """
                    Uploads file. Must be used to input tag.

                    Parameters
                    ----------


                    :param str locator: xpath/css
                    :param str locator_value: input the value of the locator as xpath of css selector
                    :param str filename: absolute path to the file.

                """
        self.locator = locator
        self.lv = locator_value
        self.filename = filename
        if self.locator == L_CSS:
            try:
                self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}").send_keys(f"{self.filename}")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv} -> {self.filename}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_XPATH:
            try:
                self.driver.find_element(By.XPATH, f"{self.lv}").send_keys(f"{self.filename}")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv} -> {self.filename}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_NAME:
            try:
                self.driver.find_element(By.NAME, f"{self.lv}").send_keys(f"{self.filename}")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv} -> {self.filename}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_LINK_TEXT:
            try:
                self.driver.find_element(By.LINK_TEXT, f"{self.lv}").send_keys(f"{self.filename}")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv} -> {self.filename}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_PARTIAL_LINK_TEXT:
            try:
                self.driver.find_element(By.PARTIAL_LINK_TEXT, f"{self.lv}").send_keys(f"{self.filename}")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv} -> {self.filename}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_TAG_NAME:
            try:
                self.driver.find_element(By.TAG_NAME, f"{self.lv}").send_keys(f"{self.filename}")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv} -> {self.filename}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_CLASS_NAME:
            try:
                self.driver.find_element(By.CLASS_NAME, f"{self.lv}").send_keys(f"{self.filename}")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv} -> {self.filename}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

    # working
    def implicit_wait(self, t):
        self.time = t
        self.driver.implicitly_wait(t)

    # working
    def explicit_wait(self, t, ac, locator, locator_value):
        """


                    Parameters
                    ----------

                    :param float t: time in seconds
                    :param str locator: xpath/css
                    :param str locator_value: input the value of the locator as xpath of css selector
                    :param str ac: action to be performed e.g. 'type'

                """
        self.time = t
        self.ac = ac
        self.locator = locator
        self.lv = locator_value
        if self.locator == L_CSS:
            if self.ac == E_CLICKABLE:
                try:
                    WebDriverWait(self.driver, self.time).until(
                        ec.element_to_be_clickable((By.CSS_SELECTOR, f"{self.lv}")))
                except TimeoutException:
                    error = NoSuchElementPresent(
                        f"{self.time} -> {self.ac} -> {self.locator} -> {self.lv}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_XPATH:
            if self.ac == E_CLICKABLE:
                try:
                    WebDriverWait(self.driver, self.time).until(ec.element_to_be_clickable((By.XPATH, f"{self.lv}")))
                except TimeoutException:
                    error = NoSuchElementPresent(
                        f"{self.time} -> {self.ac} -> {self.locator} -> {self.lv}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_NAME:
            if self.ac == E_CLICKABLE:
                try:
                    WebDriverWait(self.driver, self.time).until(ec.element_to_be_clickable((By.NAME, f"{self.lv}")))
                except TimeoutException:
                    error = NoSuchElementPresent(
                        f"{self.time} -> {self.ac} -> {self.locator} -> {self.lv}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_LINK_TEXT:
            if self.ac == E_CLICKABLE:
                try:
                    WebDriverWait(self.driver, self.time).until(ec.element_to_be_clickable((By.LINK_TEXT, f"{self.lv}")))
                except TimeoutException:
                    error = NoSuchElementPresent(
                        f"{self.time} -> {self.ac} -> {self.locator} -> {self.lv}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_PARTIAL_LINK_TEXT:
            if self.ac == E_CLICKABLE:
                try:
                    WebDriverWait(self.driver, self.time).until(ec.element_to_be_clickable((By.PARTIAL_LINK_TEXT, f"{self.lv}")))
                except TimeoutException:
                    error = NoSuchElementPresent(
                        f"{self.time} -> {self.ac} -> {self.locator} -> {self.lv}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_TAG_NAME:
            if self.ac == E_CLICKABLE:
                try:
                    WebDriverWait(self.driver, self.time).until(ec.element_to_be_clickable((By.TAG_NAME, f"{self.lv}")))
                except TimeoutException:
                    error = NoSuchElementPresent(
                        f"{self.time} -> {self.ac} -> {self.locator} -> {self.lv}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_CLASS_NAME:
            if self.ac == E_CLICKABLE:
                try:
                    WebDriverWait(self.driver, self.time).until(ec.element_to_be_clickable((By.CLASS_NAME, f"{self.lv}")))
                except TimeoutException:
                    error = NoSuchElementPresent(
                        f"{self.time} -> {self.ac} -> {self.locator} -> {self.lv}")
                    print(error.as_string())
                    assert False, f"{error.as_string()}"
            else:
                error = IllegalCharError(f"{self.ac}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

    # working
    def mouse_hover(self, locator, locator_value):
        self.locator = locator
        self.lv = locator_value
        if self.locator == L_CSS:
            self.a.move_to_element(self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}")).perform()
        elif self.locator == L_XPATH:
            self.a.move_to_element(self.driver.find_element(By.XPATH, f"{self.lv}")).perform()
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

    # working
    def right_click(self, locator, locator_value):
        self.locator = locator
        self.lv = locator_value
        if self.locator == L_CSS:
            self.a.context_click(self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}")).perform()
        elif self.locator == L_XPATH:
            self.a.context_click(self.driver.find_element(By.XPATH, f"{self.lv}")).perform()
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

    def double_click(self, locator, locator_value):
        self.locator = locator
        self.lv = locator_value
        if self.locator == L_CSS:
            self.a.double_click(self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}")).perform()
        elif self.locator == L_XPATH:
            self.a.double_click(self.driver.find_element(By.XPATH, f"{self.lv}")).perform()
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

    # working
    def shift_to_frame(self, locator, locator_value):
        self.locator = locator
        self.lv = locator_value
        if self.locator == L_CSS:
            iframe = self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}")
            self.driver.switch_to.frame(iframe)
        elif self.locator == L_XPATH:
            iframe = self.driver.find_element(By.XPATH, f"{self.lv}")
            self.driver.switch_to.frame(iframe)
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

    # working
    def leave_frame(self):
        self.driver.switch_to.default_content()

    # working
    def return_text(self, locator, locator_value):
        """
            Parameters
            ----------

            :param str locator: xpath/css
            :param str locator_value: input the value of the locator as xpath of css selector
            :return: Returns the text of the element
            :rtype: str

        """
        self.locator = locator
        self.lv = locator_value
        if self.locator == L_CSS:
            try:
                input_obj = self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_XPATH:
            try:
                input_obj = self.driver.find_element(By.XPATH, f"{self.lv}")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

        return input_obj.text

    # working
    def display_text(self, locator, locator_value):
        """
            Parameters
            ----------

            :param str locator: xpath/css
            :param str locator_value: input the value of the locator as xpath of css selector
            :return: Prints the text of the element
            :rtype: str

        """
        self.locator = locator
        self.lv = locator_value
        if self.locator == L_CSS:
            try:
                input_obj = self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_XPATH:
            try:
                input_obj = self.driver.find_element(By.XPATH, f"{self.lv}")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

        return print(input_obj.text)

    # working
    def return_attribute(self, locator, locator_value, ac_value):
        """
            Parameters
            ----------

            :param str locator: xpath/css
            :param str locator_value: input the value of the locator as xpath of css selector
            :param str ac_value: type of attribute
            :return: Returns the text of the element
            :rtype: str

        """
        self.locator = locator
        self.lv = locator_value
        self.ac_value = ac_value
        if self.locator == L_CSS:
            try:
                attribute_obj = self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}").get_attribute(
                    f"{self.ac_value}")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv} -> {self.ac_value}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_XPATH:
            try:
                attribute_obj = self.driver.find_element(By.XPATH, f"{self.lv}").get_attribute(f"{self.ac_value}")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

        return attribute_obj

    # working
    def display_attribute(self, locator, locator_value, ac_value):
        """
            Parameters
            ----------

            :param str locator: xpath/css
            :param str locator_value: input the value of the locator as xpath of css selector
            :param str ac_value: type of attribute
            :return: Prints the text of the element
            :rtype: str

        """
        self.locator = locator
        self.lv = locator_value
        self.ac_value = ac_value
        if self.locator == L_CSS:
            try:
                attribute_obj = self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}").get_attribute(
                    f"{self.ac_value}")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv} -> {self.ac_value}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_XPATH:
            try:
                attribute_obj = self.driver.find_element(By.XPATH, f"{self.lv}").get_attribute(f"{self.ac_value}")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

        return print(attribute_obj)

    # working
    def return_all_inner_text(self, locator, locator_value):
        """
                    Parameters
                    ----------

                    :param str locator: xpath/css
                    :param str locator_value: input the value of the locator as xpath of css selector
                    :return: Returns the text of the similar type element
                    :rtype: str

                """
        self.locator = locator
        self.lv = locator_value
        array_elements = []
        if self.locator == L_CSS:
            try:
                input_obj = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv}")
                if len(input_obj) == 0:
                    print(f"There are 0 checkboxes to check, try checking the locator value. ")
                for element in input_obj:
                    array_elements.append(element.text)
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_XPATH:
            try:
                input_obj = self.driver.find_elements(By.XPATH, f"{self.lv}")
                if len(input_obj) == 0:
                    print(f"There are 0 checkboxes to check, try checking the locator value. ")
                for element in input_obj:
                    array_elements.append(element.text)
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

        return array_elements

    # working
    def display_all_inner_text(self, locator, locator_value):
        """
                    Parameters
                    ----------

                    :param str locator: xpath/css
                    :param str locator_value: input the value of the locator as xpath of css selector
                    :return: Prints the text of the similar type element
                    :rtype: str

                """
        self.locator = locator
        self.lv = locator_value
        array_elements = []
        if self.locator == L_CSS:
            try:
                input_obj = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv}")
                if len(input_obj) == 0:
                    print(f"There are 0 checkboxes to check, try checking the locator value. ")
                for element in input_obj:
                    array_elements.append(element.text)
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_XPATH:
            try:
                input_obj = self.driver.find_elements(By.XPATH, f"{self.lv}")
                if len(input_obj) == 0:
                    print(f"There are 0 checkboxes to check, try checking the locator value. ")
                for element in input_obj:
                    array_elements.append(element.text)
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

        return print(array_elements)

    # working
    def is_checked_return(self, locator, locator_value):
        """
                            Parameters
                            ----------

                            :param str locator: xpath/css
                            :param str locator_value: input the value of the locator as xpath of css selector
                            :return: Prints the text of the similar type element
                            :rtype: bool

                        """
        self.locator = locator
        self.lv = locator_value
        if self.locator == L_CSS:
            try:
                attribute_obj = self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}").get_attribute("checked")
                if attribute_obj != "true":
                    return False
                else:
                    return True
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_XPATH:
            try:
                attribute_obj = self.driver.find_element(By.XPATH, f"{self.lv}").get_attribute("checked")
                if attribute_obj != "true":
                    return False
                else:
                    return True
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

    # working
    def is_checked_display(self, locator, locator_value):
        """
                            Parameters
                            ----------

                            :param str locator: xpath/css
                            :param str locator_value: input the value of the locator as xpath of css selector
                            :return: Prints the text of the similar type element
                            :rtype: bool

                        """
        self.locator = locator
        self.lv = locator_value
        if self.locator == L_CSS:
            try:
                attribute_obj = self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}").get_attribute("checked")
                if attribute_obj != "true":
                    return print("Checkbox is not checked.")
                else:
                    return print("Checkbox is checked.")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        elif self.locator == L_XPATH:
            try:
                attribute_obj = self.driver.find_element(By.XPATH, f"{self.lv}").get_attribute("checked")
                if attribute_obj != "true":
                    return print("Checkbox is not checked.")
                else:
                    return print("Checkbox is checked.")
            except NoSuchElementException:
                error = NoSuchElementPresent(
                    f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

    def is_visible_return(self, locator, locator_value):
        """
                                    Parameters
                                    ----------

                                    :param str locator: xpath/css
                                    :param str locator_value: input the value of the locator as xpath of css selector
                                    :return: Prints the text of the similar type element
                                    :rtype: bool

        """
        self.locator = locator
        self.lv = locator_value
        if self.locator == L_CSS:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}")
                if element.is_displayed():
                    return True
            except NoSuchElementException:
                return False
        elif self.locator == L_XPATH:
            try:
                element = self.driver.find_element(By.XPATH, f"{self.lv}")
                if element.is_displayed():
                    return True
            except NoSuchElementException:
                return False
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

    def is_visible_display(self, locator, locator_value):
        """
                                    Parameters
                                    ----------

                                    :param str locator: xpath/css
                                    :param str locator_value: input the value of the locator as xpath of css selector
                                    :return: Prints the text of the similar type element

        """
        self.locator = locator
        self.lv = locator_value
        if self.locator == L_CSS:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, f"{self.lv}")
                if element.is_displayed():
                    return print("Element is visible.")
            except NoSuchElementException:
                return print("Element not visible.")
        elif self.locator == L_XPATH:
            try:
                element = self.driver.find_element(By.XPATH, f"{self.lv}")
                if element.is_displayed():
                    return print("Element is visible.")
            except NoSuchElementException:
                return print("Element not visible.")
        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

    def take_pic(self):
        """
            :return: Returns the screenshot of the current webpage
         """
        image = self.driver.save_screenshot()
        return image

    def word_assert(self, obj, word):
        """

        Parameters
        ----------
        :param str obj: First string
        :param str word: Second string
        :return: Asserts True if both match else False
        :rtype: bool

        """
        self.obj = obj
        self.word = word
        if self.obj == self.word:
            assert True
        else:
            assert False

    def goto(self, url):
        """
        Changes the url to the specified url

        Parameters
        ----------
        :param str url: Url to goto

        """
        self.url = url
        is_correct_url = self.valid_url(self.url)
        self.driver.implicitly_wait(10)
        self.driver.get(f"{is_correct_url}")

    def count_div_el(self, locator, divpath):
        """
        counts the elements present in the specified div

        Parameters
        ----------
        :param str locator: xpath/css
        :param str divpath: xpath or css selector of the div element

        """
        self.divpath = divpath
        self.locator = locator
        if self.locator == L_CSS:
            count = len(self.driver.find_elements(By.CSS_SELECTOR, f"{self.divpath}"))
        elif self.locator == L_XPATH:
            count = len(self.driver.find_elements(By.XPATH, f"{self.divpath}"))
        else:
            error = IllegalCharError(f"{self.ac}")
            print(error.as_string())
            assert False, f"{error.as_string()}"
        return count

    def divcheck(self, divpath, ac, i=0):
        """
                clicks on the div elements in increasing order of xpath

                Parameters
                ----------
                :param str divpath: takes the xpath of the div
                :param str ac: action needed to be performed e.g: 'click'
                :param int i: xpath or css selector of the div element

        """
        self.divpath = divpath
        self.ac = ac
        self.i = i
        path = f"{self.divpath}"
        if ac == A_CLICK:
            self.driver.find_element(By.XPATH, f"({path})[{i + 1}]").click()

    def divtext(self, divpath, ac):
        """
                Parameters
                ----------
                :param str divpath: takes the xpath of the div
                :param str ac: action needed to be performed e.g: 'text'
                :return: Returns all the text inside the div element in increasing order of xpath
                :rtype: list


        """
        list_of_words = []
        self.divpath = divpath
        self.ac = ac
        count = len(self.driver.find_elements(By.XPATH, f"{self.divpath}"))
        # print(count)
        for a in range(count):
            path = f"{self.divpath}"
            if ac == A_TEXT:
                i = self.driver.find_element(By.XPATH, f"({path})[{a + 1}]")
                list_of_words += [i.text]
        return list_of_words

    def divtextcheck(self, divpath, ac, word):
        """
                Parameters
                ----------
                :param str divpath: takes the xpath of the div
                :param str ac: action needed to be performed e.g: 'text'
                :param str word: word that needs to be evaluated in the list of words
                :return: Returns the text of the element in increasing order of xpath and checks equality
                with the string provided.
                :rtype: bool


        """
        list_of_words = []
        self.divpath = divpath
        self.ac = ac
        self.word = word
        count = len(self.driver.find_elements(By.XPATH, f"{self.divpath}"))
        for a in range(count):
            path = f"{self.divpath}"
            if ac == A_TEXT:
                i = self.driver.find_element(By.XPATH, f"({path})[{a + 1}]")
                list_of_words += [i.text]
        if word in list_of_words:
            print("True")
        else:
            print("False")

    def homescreen(self):
        """
            Moves to the first tab and sets it as the main tab.

        """
        self.driver.implicitly_wait(10)
        parent = self.driver.window_handles[0]
        self.driver.switch_to.window(parent)
        self.driver.implicitly_wait(10)

    def childscreen(self, i=1):
        """
            Moves to the second tab and sets it as the main tab.

        """
        self.driver.implicitly_wait(10)
        self.i = i
        child = self.driver.window_handles[self.i]
        self.driver.switch_to.window(child)
        self.driver.implicitly_wait(10)

    # working
    def return_multiple_tabs_windows(self):
        """
                        :return: Returns the url of the main url sent to the webdriver.
                        :rtype: list
                """
        return self.driver.window_handles

    # working
    def display_multiple_tabs_windows(self):
        """
                        :return: Returns the url of the main url sent to the webdriver.
                        :rtype: str
                """
        return print(self.driver.window_handles)

    def closewindow(self):
        """
            CLoses the tab

        """
        self.driver.close()

    def returndivtext(self, divpath, ac, i=0):
        """
                Parameters
                ----------
                :param str divpath: takes the xpath of the div
                :param str ac: action needed to be performed e.g: 'click'
                :param int i: xpath or css selector of the div element
                :return: Returns the text of the element, can be used with increasing order of xpath
                :rtype: str

        """
        self.divpath = divpath
        self.ac = ac
        self.i = i
        path = f"{self.divpath}"
        if ac == A_TEXT:
            i = self.driver.find_element(By.XPATH, f"({path})[{i + 1}]")
        return i.text

    def cookie_click(self, locator, locator_value):
        """
            Function to specify a cookie click.
            Replicates the button function.

            Parameters
            ----------
            :param str locator: xpath/css
            :param str locator_value: input the value of the locator as xpath of css selector
        """
        self.locator = locator
        self.lv = locator_value
        if self.locator == L_CSS:
            try:
                self.button("css",
                            self.lv,
                            "click")
            except WebDriverException:
                pass
        if self.locator == L_XPATH:
            try:
                self.button("xpath",
                            self.lv,
                            "click")
            except WebDriverException:
                pass

    def end(self):
        """
            Quit the whole browser session along with all the associated browser windows

        """
        self.driver.quit()

    def title_check(self, title):
        if self.driver.title == title:
            assert True
        else:
            assert False

    def title_present(self, title):
        if self.driver.title == title:
            return True
        else:
            return False

    # working
    def check_all(self, locator, locator_value):
        """
                    Checks all checkboxes

                    Parameters
                    ----------


                    :param str locator: xpath/css
                    :param str locator_value: input the value of the locator as xpath of css selector


                """
        self.locator = locator
        self.lv = locator_value
        if self.locator == L_CSS:

            try:
                checkboxes = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv}")
                if len(checkboxes) == 0:
                    print(f"There are 0 checkboxes to check, try checking the locator value. ")
                for checkbox in checkboxes:
                    checkbox.click()
            except NoSuchElementException:
                error = NoSuchElementPresent(f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"

        elif self.locator == L_XPATH:

            try:
                checkboxes = self.driver.find_elements(By.XPATH, f"{self.lv}")
                if len(checkboxes) == 0:
                    print(f"There are 0 checkboxes to check, try checking the locator value. ")
                for checkbox in checkboxes:
                    checkbox.click()
            except NoSuchElementException:
                error = NoSuchElementPresent(f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"

        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"

    # working
    def count_all_checkboxes(self, locator, locator_value):
        """
                    Checks all checkboxes

                    Parameters
                    ----------


                    :param str locator: xpath/css
                    :param str locator_value: input the value of the locator as xpath of css selector
                    :return: Returns the number of checkboxes
                    :rtype: int

                """
        self.locator = locator
        self.lv = locator_value
        if self.locator == L_CSS:

            try:
                checkboxes = self.driver.find_elements(By.CSS_SELECTOR, f"{self.lv}")
            except NoSuchElementException:
                error = NoSuchElementPresent(f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"

        elif self.locator == L_XPATH:

            try:
                checkboxes = self.driver.find_elements(By.XPATH, f"{self.lv}")
            except NoSuchElementException:
                error = NoSuchElementPresent(f"{self.locator} -> {self.lv}")
                print(error.as_string())
                assert False, f"{error.as_string()}"

        else:
            error = IllegalCharError(f"{self.locator}")
            print(error.as_string())
            assert False, f"{error.as_string()}"
        if len(checkboxes) == 0:
            return f"0, (If it should not be 0, check the locator value."
        else:
            return len(checkboxes)
