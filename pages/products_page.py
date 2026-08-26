from .base_page import BasePage
from .product_detail_page import ProductDetailPage


class ProductsPage(BasePage):
    """Страница списка товаров /products"""

    def open_first_product(self) -> ProductDetailPage:
        """Открывает первый товар в списке (клик по 'View Product')."""
        # Устойчивый способ: первый элемент с текстом "View Product"
        first_view_product = self.page.get_by_text("View Product").first
        first_view_product.click()
        self.page.wait_for_load_state("domcontentloaded")
        return ProductDetailPage(self.page)
