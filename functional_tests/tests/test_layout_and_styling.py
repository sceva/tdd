from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.server_url)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_tag_name('input')
        window_width = self.browser.get_window_size()['width']
        print("Location is %d, Width is %d" % (inputbox.location['x'], inputbox.size['width']))
        print( "Window Width is %d" % (window_width))
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            window_width / 2,
            delta = 3
        )
        
        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_tag_name('input')
        window_width = self.browser.get_window_size()['width']
        print( "Location is %d, Width is %d" % (inputbox.location['x'], inputbox.size['width']))
        print( "Window Width is %d" % (window_width))
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            window_width / 2,
            delta = 3
        )

