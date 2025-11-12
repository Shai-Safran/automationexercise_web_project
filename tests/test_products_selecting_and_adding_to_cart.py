import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ייבוא פונקציות העזר שלך
from framework.utils import remove_all_overlays, safe_click, wait_for_clickable, hover_over_element
from framework.logger import log_info, log_warning, log_error, log_success, log_test_start, log_test_end


@pytest.mark.order(1)
def test_navigate_to_products(driver):
    test_name = "Navigate to Products"
    log_test_start(test_name)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        remove_all_overlays(driver)
        products_link = wait_for_clickable(driver, By.XPATH, "//a[contains(text(),'Products')]")
        safe_click(driver, products_link)

        log_success("ניווט לעמוד Products הצליח")
        log_test_end(test_name, "passed")
    except Exception as e:
        log_error(f"שגיאה בניווט לעמוד Products: {e}")
        log_test_end(test_name, "failed")
        assert False


@pytest.mark.order(2)
def test_click_women_category(driver):
    test_name = "Click Women Category"
    log_test_start(test_name)
    try:
        remove_all_overlays(driver)

        women_menu = wait_for_clickable(driver, By.XPATH, "//a[@href='#Women']")

        safe_click(driver, women_menu)
        log_success("לחיצה על Women בוצעה בהצלחה")

        log_test_end(test_name, "passed")
    except Exception as e:
        log_error(f"שגיאה בלחיצה על Women: {e}")
        log_test_end(test_name, "failed")
        assert False


@pytest.mark.order(3)
def test_view_blue_top_product(driver):
    test_name = "View Product (Blue Top)"
    log_test_start(test_name)

    PRODUCT_VIEW_XPATH = "//div[@class='product-image-wrapper']//a[@href='/product_details/1']"

    try:
        remove_all_overlays(driver)

        product_wrapper = wait_for_clickable(driver, By.XPATH,
                                             "//div[@class='product-image-wrapper']//p[text()='Blue Top']")
        hover_over_element(driver, product_wrapper)

        product_link = wait_for_clickable(driver, By.XPATH, PRODUCT_VIEW_XPATH)
        safe_click(driver, product_link)

        log_success("ניווט ל-Product Details הצליח")
        log_test_end(test_name, "passed")
    except Exception as e:
        log_error(f"שגיאה בפתיחת Product Details: {e}")
        log_test_end(test_name, "failed")
        assert False


@pytest.mark.order(4)
def test_add_to_cart_in_details_page(driver):
    test_name = "Add to Cart (Details Page)"
    log_test_start(test_name)

    # --- התיקון הסופי: שימוש ב-normalize-space לטיפול ברווחים ---
    ADD_TO_CART_BUTTON_XPATH = "//button[normalize-space(.)='Add to cart']"
    # -------------------------------------------------------------

    try:
        remove_all_overlays(driver)

        add_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, ADD_TO_CART_BUTTON_XPATH))
        )

        safe_click(driver, add_btn)
        log_success("לחיצה על Add to Cart בוצעה בהצלחה")

        remove_all_overlays(driver)

        popup_text = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Your product has been added to cart.')]"))
        )

        if popup_text:
            log_success("Popup Add to Cart הופיע בהצלחה")
            log_test_end(test_name, "passed")
        else:
            log_error("Popup לא הופיע לאחר לחיצה על Add to Cart")
            log_test_end(test_name, "failed")
            assert False
    except Exception as e:
        log_error(f"שגיאה במהלך הוספה לעגלה: {e}")
        log_test_end(test_name, "failed")
        assert False