import os
from functools import partial

import gradio as gr

from app.src.entities.init_db import init_collection, init_images
from app.src.processing.models import get_models
from app.src.processing.tasks import generate_outputs_args, save_original_art_args


def main():
    init_collection()

    processor, model, emb_model = get_models()
    init_images(emb_model)
    generate_outputs = partial(generate_outputs_args, processor_=processor, model_=model, emb_model_=emb_model)

    save_original_art = partial(save_original_art_args, emb_model=emb_model)

    with gr.Blocks() as demo:

        with gr.Tab(label="Check Original Art"):
            with gr.Column():
                gr.Interface(
                    generate_outputs,
                    inputs=[gr.Image(label="Insert Image", type="filepath"), gr.Textbox(label='Description')],
                    outputs=[gr.Textbox(label="Title"), gr.Textbox(label="Score"),
                             gr.Textbox(label="Description used"), gr.Image(label="Closest Image from DB", type="filepath")],
                    allow_flagging="never"
                )
        with gr.Tab(label="Save Original Art"):
            with gr.Column():
                gr.Interface(
                    save_original_art,
                    inputs=[gr.Files(label="Insert Image"), gr.Textbox(label='Title'),
                            gr.Textbox(label='Author'), gr.Textbox(label='description')],
                    outputs=gr.Textbox(label="Results"),
                    allow_flagging="never"
                )

    demo.launch(
        share=os.environ["SHARE"].lower() == "true",
        debug=os.environ["DEBUG"].lower() == "true",
        server_port=int(os.environ["SERVER_PORT"]),
        server_name=os.environ["SERVER_NAME"]
    )


if __name__ == "__main__":
    main()
