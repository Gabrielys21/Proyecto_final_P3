import tkinter as tk
from agents import chat_with_gpt, send_whatsapp_message

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot Interface")

        self.chat_log = tk.Text(root, state='disabled', width=50, height=20, bg='light grey')
        self.chat_log.pack(pady=10)

        self.entry_box = tk.Entry(root, width=50)
        self.entry_box.pack(pady=5)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

    def send_message(self):
        user_message = self.entry_box.get()
        self.entry_box.delete(0, tk.END)

        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, "You: " + user_message + "\n")

        gpt_response = chat_with_gpt(user_message)
        self.chat_log.insert(tk.END, "Bot: " + gpt_response + "\n")
        self.chat_log.config(state='disabled')

        # Example of sending a message via WhatsApp
        # send_whatsapp_message("whatsapp_number", gpt_response)

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatbotGUI(root)
    root.mainloop()