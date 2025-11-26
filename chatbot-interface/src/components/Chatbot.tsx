import Header from './Header.tsx';
import { useEffect, useRef, useState } from 'react';
import InputField from './InputField.tsx';
import ReactMarkdown from 'react-markdown';
import { FaSpinner } from 'react-icons/fa';
import { RiRobot3Fill } from 'react-icons/ri';

interface RasaEvent {
  event: string,
  text: string
}

/**
 * Component that renders the chatbot interface
 */
export default function Chatbot() {
  const [showInterface, setShowInterface] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const [chats, setChats] = useState<{prompt: string, response: string|null}[]>([]);
  const messagesEndRef = useRef<HTMLDivElement|null>(null);

  useEffect(() => {
    const params = new URLSearchParams();
    params.set('userId', '1');

    fetch(`http://localhost:5005/conversations/test_user/tracker`)
      .then(response => response.json())
      .then(data => {
          const messages: {prompt: string, response: string}[] = []
          let currentPrompt: null | string;

          data.events.forEach((event: RasaEvent) => {
              if (event.event === 'user') {
                  currentPrompt = event.text;
              } else if (event.event === 'bot' && currentPrompt) {
                  messages.push({
                      prompt: currentPrompt,
                      response: event.text
                  });
                  currentPrompt = null;
              }
          });
          setChats(messages);
      });
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({behavior: 'smooth'});
  }, [chats]);

  function changeInterface() {
    setShowInterface(prev => !prev);
  }

  if (showInterface) {
    return <div className={'chatbot-interface'}>
      <Header closeFunction={changeInterface}/>
      <div className={'chats'}>
        {
          chats.length === 0 ?
            <p className={'info-text'}>Hello there 👋! I am Kabarak University's official AI assistant 🤖. How may I
              assist you today?</p> :
            <>{chats.map((chat, index) => {
              const isLastChat = index === chats.length - 1;

              return (
                <div key={index}>
                  <p className={'prompt'}>{chat.prompt}</p>
                  {chat.response ? (
                    <p className={'response'}>
                      <ReactMarkdown>{chat.response}</ReactMarkdown>
                    </p>
                  ) : isThinking && isLastChat ? (
                    <div className={'thinking'}>
                      <FaSpinner className="spin"/>
                      <p>thinking...</p>
                    </div>
                  ) : null}
                </div>
              );
            })}
              <div ref={messagesEndRef}></div>
            </>
        }
      </div>
      <InputField animation={setIsThinking} addChat={setChats} previousChats={chats}/>
    </div>;
  } else {
    return <RiRobot3Fill className={'chatbot-widget'} onClick={changeInterface}/>;
  }
}