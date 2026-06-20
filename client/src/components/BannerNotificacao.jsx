export default function BannerNotificacao({ bannerAtivo, onFechar }) {
  if (!bannerAtivo) return null;
  return (
    <div data-cy="banner-notificacao" style={{
      position: 'fixed', top: '20px', left: '50%', transform: 'translateX(-50%)',
      backgroundColor: '#007bff', color: '#fff', padding: '15px 25px',
      borderRadius: '8px', zIndex: 9999, maxWidth: '400px'
    }}>
      <strong>{bannerAtivo.remetente}:</strong> {bannerAtivo.texto}
      <button onClick={onFechar} style={{ marginLeft: '15px', background: 'transparent', border: 'none', color: '#fff' }}>×</button>
    </div>
  );
}