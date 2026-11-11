"""No-JS and assistive-technology basics for mobile navigation."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
H=(ROOT/"index.html").read_text()
JS=(ROOT/"main.js").read_text()

class MobileNavigationContract(unittest.TestCase):
    def test_button_has_state_and_controls_reference(self):
        self.assertIn('aria-controls="mobile-menu"',H)
        self.assertIn('aria-expanded="false"',H)
        self.assertIn('id="mobile-menu"',H)
    def test_click_and_link_activation_keep_expanded_state_in_sync(self):
        self.assertIn("setAttribute('aria-expanded', String(menuBtn.classList.contains('active')))",JS)
        self.assertIn("setAttribute('aria-expanded', 'false')",JS)

if __name__=="__main__":
    unittest.main()
