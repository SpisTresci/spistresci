from spistresci.behave.adapter.selenium.base import BaseSeleniumAdapter


class NavigationBarSeleniumAdapter(BaseSeleniumAdapter):

    def service_name_in_navbar_match_current_service(self):
        menu = self.browser.find_element_by_xpath("//ul[@class='menu']")
    
        a_elements = menu.find_elements_by_xpath(
            "li[not(contains(@class, 'menu2'))]/a"
        )
    
        self.data = {
            'marked_as_active': [],
        }
    
        for a in a_elements:
            if a.get_attribute('href') in self.browser.current_url:
                self.data['marked_as_active'].append(a)

    def check_marked_as_active_services(self):
        for item in self.data['marked_as_active']:
            li_element = item.find_element_by_xpath('..')
            assert li_element.get_attribute('class'), 'act'
