from django.core.urlresolvers import resolve
from django.test import Client, TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from lists.models import Item, List
from lists.views import home_page
from lists.forms import ItemForm, EMPTY_LIST_ERROR

class HomePageTest(TestCase):
        
    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.all().count(), 0)
        
        
class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)
        
        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_displays_all_items(self):
       list_ = List.objects.create()
       Item.objects.create(text='itemey 1', list=list_)
       Item.objects.create(text='itemey 2', list=list_)

    def test_list_view_passes_correct_list_to_list_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(response.context['list'], correct_list)
    
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={ 'text': 'A new item for an existing list' }
        )

        self.assertEqual(Item.objects.all().count(), 1)
        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data = {'text': "A new item for an existing list"}
        )
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
                '/lists/%d/' % (list_.id,),
                data = {'text': ''}
        )
    
    def test_invalid_input_means_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.all().count(), 0)
        
    def test_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertTemplateUsed(response, 'list.html')

    def test_invalid_input_renders_with_form_errors(self):
    	response = self.post_invalid_input()
    	self.assertContains(response, escape(EMPTY_LIST_ERROR))
    	        
    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        response = self.client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )
        self.assertEqual(Item.objects.all().count(), 1)
        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new list item')
        self.assertEqual(List.objects.all().count(), 1)
        new_list = List.objects.all()[0]
        self.assertEqual(new_item.list, new_list)

        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

    def test_validation_errors_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ""})
        self.assertEqual(Item.objects.all().count(), 0)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, escape(EMPTY_LIST_ERROR))
        self.assertIsInstance(response.context['form'], ItemForm)

