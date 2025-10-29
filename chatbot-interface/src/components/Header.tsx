interface HeaderProps {
  closeFunction: () => void;
}

/**
 * Component that renders the header of the chat interface
 * @param closeFunction Function to be triggered when the close button is clicked
 */
export default function Header({closeFunction}: HeaderProps) {
  return <div className={'chatbot-header'}>
    <img src={'https://kabarak.ac.ke/images/logos/logo-retina1.png'} alt={'Kabarak Logo'}/>
    <h1>KabuAssist</h1>
    <p onClick={closeFunction}>&times;</p>
  </div>;
}