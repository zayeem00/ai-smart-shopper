# interface.py
import gradio as gr
from recommendations import recommend_products, generate_contextual_message
from utils import process_csv

css = """
.lg.svelte-cmf5ev {background-color: #8A2BE2 !important;}
.user.svelte-1pjfiar.svelte-1pjfiar.svelte-1pjfiar {padding: 7px !important;border-radius: 10px 10px 0px 10px;width: fit-content;background-color: #E6E6FA !important ;border-color:#E6E6FA !important}
.bot.svelte-1pjfiar.svelte-1pjfiar.svelte-1pjfiar {padding: 7px !important;border-radius: 10px 10px 10px 0px;width : fit-content !important;border: 1.5px solid #9370DB !important;background: #FFFFFF 0% 0% no-repeat padding-box !important;box-shadow: 0px 3px 6px #0000001A !important;border: 2px solid #9370DB !important;}
.primary.svelte-cmf5ev {box-shadow: 0px 3px 6px #0000001A !important;border: 2px solid #9370DB !important;background: #8A2BE2 !important;width: fit-content;}
.primary.svelte-cmf5ev {color: white !important}
textarea.scroll-hide.svelte-1f354aw {font-family:'Roboto','Arial',sans-serif;font-size:14px}
label.svelte-1b6s6s { background: #9370DB 0% 0% no-repeat padding-box;color: white;width: 100%;}
label.svelte-1b6s6s {background: #9370DB 0% 0% no-repeat padding-box;color: white;width: 100%;font-size:20px;font-family:'Roboto','Arial',sans-serif; border-radius: 0px 0px 10px 10px;}
.wrapper.svelte-nab2ao{background-color : #F7F7F7 }
svg.iconify.iconify--carbon{width:15px; height:15px}
.thumbnail-item.svelte-fiatpe.svelte-fiatpe:hover {--ring-color: #9370DB !important;}
"""

default_chat = [["Welcome! I'm your AI-powered product recommendation bot. Ask me anything about finding the perfect product for you.", "I'm here to assist you with any product-related inquiries. Let's find what you need!"]]

# Gradio interface functions
def handle_file_upload(file, openai_api_key, pinecone_api_key, pinecone_env):
    return process_csv(file, openai_api_key, pinecone_api_key, pinecone_env)

def display_recommendations(user_input, openai_api_key, pinecone_api_key, pinecone_env, system_prompt):
    recommendations = recommend_products(user_input, openai_api_key, pinecone_api_key, pinecone_env)
    contextual_message = generate_contextual_message(user_input, recommendations, openai_api_key, system_prompt)
    return recommendations, contextual_message

def update_outputs(query_input, openai_api_key, pinecone_api_key, pinecone_env, chat_history, system_prompt):
    recommendations, contextual_message = display_recommendations(query_input, openai_api_key, pinecone_api_key, pinecone_env, system_prompt)
    
    # Update chat history
    new_chat_history = chat_history + [[query_input, contextual_message]]
    
    return recommendations, new_chat_history, gr.update(value="")

# Create Gradio Interface
def build_interface():
    with gr.Blocks(title="AI Smart Shopper", head="True", css=css) as interface:
        gr.Markdown("""<div style="text-align: center; font-weight: bold;"> <h1>AI Smart Shopper</h1> </div>""")
        
        with gr.Tab("API Keys"):
            openai_api_key_input = gr.Textbox(label="OpenAI API Key", type="password")
            pinecone_api_key_input = gr.Textbox(label="Pinecone API Key", type="password")
            pinecone_env_input = gr.Textbox(label="Pinecone Environment", placeholder="e.g., us-east-1")
            system_prompt_input = gr.Textbox(label="System Prompt", placeholder="Enter a system prompt for the assistant...")

        with gr.Tab("Upload Catalog"):
            upload_button = gr.File(label="Upload CSV", type="filepath")
            output = gr.Textbox()
            upload_button.upload(handle_file_upload, inputs=[upload_button, openai_api_key_input, pinecone_api_key_input, pinecone_env_input], outputs=output)
        
        with gr.Tab("Get Recommendations"):
            with gr.Row():
                with gr.Column(scale=1):
                    chatbot = gr.Chatbot(value=default_chat, label="Recommender Chatbot", show_label=True)
                    query_input = gr.Textbox(label="Enter your product preference...", show_label=False, placeholder="Type your query here...")
                    with gr.Row():
                        with gr.Column(scale=1, min_width=150):
                            recommend_button = gr.Button("Get Recommendations")
                        with gr.Column(scale=1, min_width=150):
                            clear_button = gr.Button("Clear")
                    # Define state for chat history
                    chat_history = gr.State([])

                    # Define outputs
                with gr.Column(scale=1):
                    recommendations_output = gr.Gallery(label="Recommendations For You", show_label=False, elem_id="gallery", columns=[3], rows=[1], object_fit="contain", height="auto", scale=5)

                recommend_button.click(
                    update_outputs,
                    inputs=[query_input, openai_api_key_input, pinecone_api_key_input, pinecone_env_input, chat_history, system_prompt_input],
                    outputs=[recommendations_output, chatbot, query_input]
                )

                clear_button.click(
                    lambda: (gr.update(value=default_chat), gr.update(value=""), gr.update(value=[]), gr.update(value=[])),
                    outputs=[chatbot, query_input, chat_history, recommendations_output]
                )
                
    return interface
