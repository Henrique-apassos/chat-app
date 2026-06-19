import { useState, useEffect } from 'react';

export function useMobile(breakpoint = 768) {
    const [isMobile, setIsMobile] = useState(window.innerWidth <= breakpoint);

    useEffect(() => {
        const handleResize = () => setIsMobile(window.innerWidth <= breakpoint);
        
        // Ouve o redimensionamento da janela do navegador
        window.addEventListener('resize', handleResize);
        
        // Limpeza do evento
        return () => window.removeEventListener('resize', handleResize);
    }, [breakpoint]);

    return isMobile;
}