export default function BadgeNotificacao({ quantidade }) {
    if (!quantidade || quantidade === 0) return null;
    
    return (
        <span
            data-cy="badge-notificacao"
            style={{
                backgroundColor: '#ff3b30',
                color: '#fff',
                borderRadius: '10px',
                padding: '2px 8px',
                fontSize: '0.75rem',
                fontWeight: 'bold',
                marginLeft: '8px',
                minWidth: '20px',
                textAlign: 'center',
                display: 'inline-block'
            }}
        >
            {quantidade > 99 ? '99+' : quantidade}
        </span>
    );
}