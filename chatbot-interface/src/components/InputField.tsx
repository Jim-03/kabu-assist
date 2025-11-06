import { BsFillSendFill } from 'react-icons/bs';
import { type FormEvent, useEffect, useState } from 'react';

interface InputFieldProps {
  animation: (value: ( ( (prevState: boolean) => boolean )|boolean )) => void,
  addChat: (value: ( ( (prevState: {prompt: string; response: string|null}[]) => {
    prompt: string;
    response: string|null
  }[] )|{prompt: string; response: string|null}[] )) => void,
  previousChats: {prompt: string; response: string|null}[]
}

/**
 * Component that renders the input field in the chatbot's interface
 * @param animation A function that controls the display of thinking animation
 * @param addChat A function that adds a new chat to the chats array
 * @param previousChats An array of previous chats
 */
export default function InputField({animation, addChat, previousChats}: InputFieldProps) {
  const [promptText, setPromptText] = useState<string>('');

  /**
   * Sends a user's prompt from the input field to the backend service
   */
  function sendPrompt() {
    if (!promptText) return;

    const currentPrompt = promptText;

    addChat([...previousChats, {prompt: currentPrompt, response: null}]);
    animation(true);
    setPromptText('');

    fetch('http://localhost:5005/webhooks/rest/webhook', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        sender: "test_user",
        message: currentPrompt
      })
    })
      .then((response) => response.json())
      .then((data) => {
        const responses: string[] = []

        data.forEach(response => {
          responses.push(response.text)
        })

        addChat((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            response: responses.join('\n\n')
          };
          return updated;
        });
      })
      .catch((err) => console.error('Chat error:', err))
      .finally(() => setTimeout(() => animation(false), 300));
  }

  /**
   * Handles the form submission
   * @param e Keyboard event
   */
  function submitPrompt(e: FormEvent) {
    e.preventDefault();
    sendPrompt();
  }

  useEffect(() => {
    /**
     * Triggered when the 'Enter' key is pressed
     */
    function sendWhenEnterIsClicked(e: KeyboardEvent) {
      if (e.code === 'Enter') {
        sendPrompt();
      }
    }

    document.addEventListener('keydown', sendWhenEnterIsClicked);

    return () => document.removeEventListener('keydown', sendWhenEnterIsClicked);
  }, []);

  return (
    <form onSubmit={submitPrompt} className={'chatbot-input'}>
      <input type={'text'} placeholder={'Type a message'} onChange={e => setPromptText(e.target.value)}
             value={promptText}/>
      <button type="submit" disabled={!promptText}>
        <BsFillSendFill className={'send-button'}/>
      </button>
    </form>
  );
}