""" 
Bubble sort visualizer with step-by-step trace
Author:  Pranav Tripathi
Student Number: 20388092
Date:  April 2026
""" 

import gradio as gr

def bubble_sort_steps(numbers):
    arr = numbers[:] # copy so we dont touch the original
    steps = []
    n = len(arr)

    steps.append("Starting array: " + str(arr))

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            # compare neighbours
            steps.append("Pass " + str(i + 1) + " | Comparing index " + str(j) + " (" + str(arr[j]) + ") and index " + str(j + 1) + " (" + str(arr[j + 1]) + ")")

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                steps.append("  -> Swapped! Array is now: " + str(arr))
            else:
                steps.append("  -> No swap needed")

        # largest unsorted element is now at the end of this pass
        steps.append("End of pass " + str(i + 1) + ": " + str(arr) + "  (position " + str(n - i - 1) + " is sorted)")

        # early exit if nothing swapped this pass
        if not swapped:
            steps.append("No swaps this pass - array already sorted, stopping early")
            break

    steps.append("\nFinal sorted array: " + str(arr))
    return steps, arr


def run_sort(user_input):
    # make sure something was entered
    if not user_input.strip():
        return "Please enter some numbers", ""

    # parse input, catch non-integer values
    try:
        numbers = [int(x.strip()) for x in user_input.split(",") if x.strip()]
    except ValueError:
        return "Invalid input - enter integers separated by commas (e.g. 5, 3, 8, 1)", ""

    # need at least 2 to sort
    if len(numbers) < 2:
        return "Enter at least 2 numbers", ""

    # cap at 20 so output stays readable
    if len(numbers) > 20:
        return "Enter 20 numbers or fewer", ""

    steps, sorted_arr = bubble_sort_steps(numbers)

    step_log = "\n".join(steps)
    result = ", ".join(str(x) for x in sorted_arr)

    return step_log, result


# build the UI
with gr.Blocks(title="Bubble Sort Visualizer", theme=gr.themes.Soft()) as demo:

    gr.Markdown("# Bubble Sort Visualizer\nEnter a list of integers and watch bubble sort work through them step by step")

    with gr.Row():

        with gr.Column(scale=1):
            number_input = gr.Textbox(
                label="Enter numbers (comma-separated)",
                placeholder="e.g. 5, 3, 8, 1, 9, 2",
                lines=2
            )
            sort_btn = gr.Button("Run Bubble Sort", variant="primary")

            # pre-loaded examples including best and worst case
            gr.Examples(
                examples=[
                    ["5, 3, 8, 1, 9, 2"],
                    ["10, 7, 3, 1"],
                    ["1, 2, 3, 4, 5"],   # already sorted - triggers early exit
                    ["5, 4, 3, 2, 1"],   # reverse sorted - worst case
                ],
                inputs=number_input,
                label="Try an example"
            )

        with gr.Column(scale=2):
            result_output = gr.Textbox(label="Sorted Result", interactive=False, lines=1)
            steps_output = gr.Textbox(label="Step-by-Step Trace", interactive=False, lines=20)

    # wire button to sort function
    sort_btn.click(fn=run_sort, inputs=number_input, outputs=[steps_output, result_output])

    gr.Markdown("""---
### How Bubble Sort works
Repeatedly walks through the list comparing adjacent pairs and swapping them if out of order.
After each pass the largest unsorted element is in its final position.
Stops early if a full pass produces zero swaps.

**Time complexity:** O(n²) average/worst | O(n) best (already sorted)""")

demo.launch()
