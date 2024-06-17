import PySimpleGUI as sg


def custom_popup(title, message, bg_color):
    # Define the window's layout with a matching background color for the text element
    layout = [
        [sg.Text(message, background_color=bg_color, text_color='BLACK', font=('Helvetica', 42), justification='center', expand_x=True, pad=(0, 0), key='-MESSAGE-')]
    ]

    # Create the window with a uniform background color and keep_on_top set to True
    window = sg.Window(title, layout, background_color=bg_color, element_justification='c', margins=(300, 250), keep_on_top=True, return_keyboard_events=True,  use_default_focus=False, finalize=True)
    # Force the window to take focus
    window.TKroot.focus_force()

    # Event loop to display the window and listen for the Enter key
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '\r':  # Check for window close or Enter key
            break

    # Close the window
    window.close()


def prompt_label():
    # Define the layout of the window
    layout = [[sg.Text('Label contents')],
              [sg.InputText(key='-INPUT-')],  # Input field for text with a key
              [sg.Submit(), sg.Cancel()]]  # Buttons for submitting or cancelling

    # Create the window with the specified layout and finalize to modify before the loop
    window = sg.Window('KT-400 Label Scanner', layout, finalize=True)

    # Force the window to take focus
    window.TKroot.focus_force()
    # Set focus on the input text box
    window['-INPUT-'].set_focus()

    # Event loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):  # If user closes window or clicks cancel
            user_input = None
            break
        if event == 'Submit':
            user_input = values['-INPUT-']  # Save the input text into a variable
            break  # Close the window after submission

    window.close()
    return user_input