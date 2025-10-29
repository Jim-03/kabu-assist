/**
 * Component that serves Kabarak university's landing page
 */
export default function LandingPage() {
  return <div>
    <iframe src={'../../public/landing.html'}
            style={{width: '100%', height: '100vh', border: 'none'}}
    />
  </div>;
}