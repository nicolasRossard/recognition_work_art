import os
from functools import partial

import gradio as gr
from app.src.entities.init_db import init_collection, init_images_os
from app.src.processing.models import get_models
from app.src.processing.tasks import generate_description_args


def generate_description_interface():
    init_collection()

    processor, model, _ = get_models()
    generate_description = partial(generate_description_args, processor_=processor, model_=model)

    with gr.Blocks() as tabs:

        with gr.Tab(label="Generate Description"):
            with gr.Column():
                gr.Interface(
                    generate_description,
                    inputs=[gr.Image(label="Insert Image", type="filepath")],
                    outputs=gr.Textbox(label="Score"),
                    allow_flagging="never"
                )

    return tabs


if __name__ == "__main__":
    processor, model, emb_model = get_models()
    collection = 'os_description'
    init_collection(collection=collection)
    init_images_os(processor, model, emb_model)
    interface = generate_description_interface()
    interface.launch(
        share=os.environ["SHARE"].lower() == "true",
        debug=os.environ["DEBUG"].lower() == "true",
        server_port=int(os.environ["SERVER_PORT"]),
        server_name=os.environ["SERVER_NAME"]
    )