from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
class Contact:
    def __init__(self, name, phone_number, email, address):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address
class ContactManagerApp(App):
    contacts = []
    def build(self):
        self.title = 'Contact Manager'
        self.current_contact = None
        self.layout = BoxLayout(orientation='horizontal', spacing=10, padding=10)
        self.left_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.5, 1))
        self.info_label = Label(text="Contact Information", size_hint=(1, None), height=30, font_size=20)
        self.left_layout.add_widget(self.info_label)
        self.name_input = TextInput(hint_text='Name', multiline=False, font_size=16)
        self.phone_input = TextInput(hint_text='Phone Number', multiline=False, font_size=16)
        self.email_input = TextInput(hint_text='Email', multiline=False, font_size=16)
        self.address_input = TextInput(hint_text='Address', multiline=False, font_size=16)
        self.left_layout.add_widget(self.name_input)
        self.left_layout.add_widget(self.phone_input)
        self.left_layout.add_widget(self.email_input)
        self.left_layout.add_widget(self.address_input)
        self.button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=50)
        self.add_button = Button(text='Add Contact', on_press=self.add_contact, font_size=16)
        self.update_button = Button(text='Update Contact', on_press=self.update_contact, font_size=16)
        self.search_button = Button(text='Search', on_press=self.search_contacts, font_size=16)
        self.delete_button = Button(text='Delete Contact', on_press=self.delete_contact, font_size=16)
        self.clear_button = Button(text='Clear Fields', on_press=self.clear_fields, font_size=16)
        self.button_layout.add_widget(self.add_button)
        self.button_layout.add_widget(self.update_button)
        self.button_layout.add_widget(self.search_button)
        self.button_layout.add_widget(self.delete_button)
        self.button_layout.add_widget(self.clear_button)
        self.left_layout.add_widget(self.button_layout)
        self.right_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.5, 1))
        self.contact_list_label = Label(text="Contacts", size_hint=(1, None), height=30, font_size=20)
        self.right_layout.add_widget(self.contact_list_label)
        self.contact_list_view = ScrollView()
        self.contact_list_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.contact_list_layout.bind(minimum_height=self.contact_list_layout.setter('height'))
        self.contact_list_view.add_widget(self.contact_list_layout)
        self.right_layout.add_widget(self.contact_list_view)
        self.layout.add_widget(self.left_layout)
        self.layout.add_widget(self.right_layout)
        self.contacts.extend([
            Contact("John Doe", "123-456-7890", "john.doe@example.com", "123 Main St"),
            Contact("Jane Smith", "456-789-0123", "jane.smith@example.com", "456 Elm St")
        ])
        self.update_contact_list()
        return self.layout
    def add_contact(self, instance):
        name = self.name_input.text.strip()
        phone_number = self.phone_input.text.strip()
        email = self.email_input.text.strip()
        address = self.address_input.text.strip()
        if name and phone_number:
            contact = Contact(name, phone_number, email, address)
            self.contacts.append(contact)
            self.update_contact_list()
            self.show_popup("Contact Added", f"Contact '{name}' added successfully.")
            self.clear_fields()
        else:
            self.show_popup("Error", "Name and Phone Number are required fields.")
    def update_contact(self, instance):
        if self.current_contact:
            name = self.name_input.text.strip()
            phone_number = self.phone_input.text.strip()
            email = self.email_input.text.strip()
            address = self.address_input.text.strip()
            self.current_contact.name = name
            self.current_contact.phone_number = phone_number
            self.current_contact.email = email
            self.current_contact.address = address
            self.update_contact_list()
            self.show_popup("Contact Updated", f"Contact '{name}' updated successfully.")
        else:
            self.show_popup("Error", "Select a contact from the list to update.")
    def search_contacts(self, instance):
        keyword = self.name_input.text.strip().lower()
        if keyword:
            results = [contact for contact in self.contacts if keyword in contact.name.lower()]
            self.update_contact_list(results)
        else:
            self.update_contact_list()
    def delete_contact(self, instance):
        if self.current_contact:
            self.contacts.remove(self.current_contact)
            self.update_contact_list()
            self.show_popup("Contact Deleted", f"Contact '{self.current_contact.name}' deleted successfully.")
            self.clear_fields()
        else:
            self.show_popup("Error", "Select a contact from the list to delete.")
    def update_contact_list(self, contacts=None):
        self.contact_list_layout.clear_widgets()
        if not contacts:
            contacts = self.contacts
        for contact in contacts:
            contact_btn = Button(text=f"{contact.name}: {contact.phone_number}", size_hint_y=None, height=40, font_size=16)
            contact_btn.bind(on_press=lambda btn: self.select_contact(contact))
            self.contact_list_layout.add_widget(contact_btn)
    def select_contact(self, contact):
        self.current_contact = contact
        self.name_input.text = contact.name
        self.phone_input.text = contact.phone_number
        self.email_input.text = contact.email
        self.address_input.text = contact.address
    def clear_fields(self, instance=None):
        self.name_input.text = ''
        self.phone_input.text = ''
        self.email_input.text = ''
        self.address_input.text = ''
        self.current_contact = None
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()
if __name__ == '__main__':
    ContactManagerApp().run()
