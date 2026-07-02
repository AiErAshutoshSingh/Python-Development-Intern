import React, { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars, Float, Sphere, MeshDistortMaterial } from '@react-three/drei';
import { Activity, Zap, DollarSign, TrendingUp } from 'lucide-react';
import axios from 'axios';

/* ─── 3D Background Scene ─────────────────────────────────────── */
const Background = () => (
  <>
    <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
    <ambientLight intensity={0.4} />
    <directionalLight position={[10, 10, 10]} intensity={1} color="#00f0ff" />
    <pointLight position={[-10, -10, -10]} intensity={1} color="#ff003c" />

    {/* Floating cyan orb */}
    <Float speed={1.5} rotationIntensity={1} floatIntensity={2}>
      <Sphere args={[1, 64, 64]} position={[-4, 0.5, -5]}>
        <MeshDistortMaterial color="#00f0ff" metalness={0.8} roughness={0.2} distort={0.4} speed={2} clearcoat={1} />
      </Sphere>
    </Float>

    {/* Floating red orb */}
    <Float speed={2} rotationIntensity={2} floatIntensity={1.5}>
      <Sphere args={[0.7, 64, 64]} position={[4.5, 2, -3]}>
        <MeshDistortMaterial color="#ff003c" metalness={0.8} roughness={0.2} distort={0.5} speed={3} clearcoat={1} />
      </Sphere>
    </Float>

    {/* Small blue orb */}
    <Float speed={1} rotationIntensity={0.5} floatIntensity={3}>
      <Sphere args={[0.4, 64, 64]} position={[2, -2, -4]}>
        <MeshDistortMaterial color="#0055ff" metalness={0.9} roughness={0.1} distort={0.6} speed={4} clearcoat={1} />
      </Sphere>
    </Float>

    <OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={0.4} />
  </>
);

/* ─── Status Badge ────────────────────────────────────────────── */
const StatusBadge = ({ status }: { status: string }) => {
  const connected = status === 'connected';
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: 6,
      background: connected ? 'rgba(0,240,255,0.1)' : 'rgba(255,0,60,0.1)',
      border: `1px solid ${connected ? '#00f0ff' : '#ff003c'}`,
      color: connected ? '#00f0ff' : '#ff003c',
      borderRadius: 20, padding: '2px 12px', fontSize: 12, fontWeight: 700,
      textTransform: 'uppercase', letterSpacing: 1,
    }}>
      <span style={{
        width: 6, height: 6, borderRadius: '50%',
        background: connected ? '#00f0ff' : '#ff003c',
        boxShadow: connected ? '0 0 6px #00f0ff' : '0 0 6px #ff003c',
        animation: connected ? 'pulse 1.5s infinite' : 'none',
      }} />
      {status}
    </span>
  );
};

/* ─── Input Component ─────────────────────────────────────────── */
const Field = ({ label, children }: { label: string; children: React.ReactNode }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
    <label style={{ fontSize: 12, color: '#94a3b8', textTransform: 'uppercase', letterSpacing: 1 }}>{label}</label>
    {children}
  </div>
);

const inputStyle: React.CSSProperties = {
  width: '100%', boxSizing: 'border-box',
  background: 'rgba(0,0,0,0.4)',
  border: '1px solid rgba(255,255,255,0.12)',
  borderRadius: 8, padding: '10px 14px',
  color: 'white', fontSize: 14, fontFamily: 'inherit',
  outline: 'none', transition: 'border-color 0.2s',
};

/* ─── Main App ────────────────────────────────────────────────── */
export default function App() {
  const [status, setStatus] = useState<string>('checking...');
  const [symbol, setSymbol] = useState('BTCUSDT');
  const [side, setSide] = useState<'BUY' | 'SELL'>('BUY');
  const [orderType, setOrderType] = useState('MARKET');
  const [quantity, setQuantity] = useState('0.001');
  const [price, setPrice] = useState('');
  const [stopPrice, setStopPrice] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<{ success: boolean; msg: string } | null>(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/status')
      .then(res => setStatus(res.data.status))
      .catch(() => setStatus('disconnected'));
  }, []);

  const handleTrade = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);
    try {
      const payload: Record<string, unknown> = {
        symbol, side, order_type: orderType,
        quantity: parseFloat(quantity),
      };
      if (orderType !== 'MARKET') payload.price = parseFloat(price);
      if (orderType === 'STOP') payload.stop_price = parseFloat(stopPrice);

      const res = await axios.post('http://127.0.0.1:8000/place-order', payload);
      setResponse({ success: true, msg: `✅ Order placed! ID: ${res.data.data.orderId} | Status: ${res.data.data.status}` });
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } }; message?: string })?.response?.data?.detail ?? (err as { message?: string })?.message ?? 'Unknown error';
      setResponse({ success: false, msg: `❌ ${msg}` });
    } finally {
      setLoading(false);
    }
  };

  const isBuy = side === 'BUY';
  const btnGradient = isBuy
    ? 'linear-gradient(135deg, #00f0ff, #0055ff)'
    : 'linear-gradient(135deg, #ff003c, #ff6b00)';

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative', overflow: 'hidden', fontFamily: 'Inter, sans-serif' }}>
      {/* Animated CSS for the pulse */}
      <style>{`
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
        input:focus, select:focus { border-color: #00f0ff !important; box-shadow: 0 0 0 2px rgba(0,240,255,0.15); }
        select option { background: #0a0a0f; }
      `}</style>

      {/* 3D Canvas Background */}
      <div style={{ position: 'absolute', inset: 0, zIndex: 0 }}>
        <Canvas camera={{ position: [0, 0, 10] }}>
          <Background />
        </Canvas>
      </div>

      {/* Dark gradient overlay */}
      <div style={{
        position: 'absolute', inset: 0, zIndex: 1,
        background: 'radial-gradient(ellipse at center, rgba(10,10,15,0.4) 0%, rgba(10,10,15,0.75) 100%)',
      }} />

      {/* UI Layer */}
      <div style={{
        position: 'absolute', inset: 0, zIndex: 2,
        display: 'flex', flexDirection: 'column', padding: 24, gap: 16,
        overflowY: 'auto',
      }}>
        {/* Header */}
        <div className="glass-panel" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{
              width: 40, height: 40, borderRadius: '50%',
              background: 'linear-gradient(135deg, #00f0ff, #0055ff)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              boxShadow: '0 0 20px rgba(0,240,255,0.4)',
            }}>
              <TrendingUp size={20} color="white" />
            </div>
            <div>
              <h1 style={{ margin: 0, fontSize: 20, fontWeight: 800, color: '#fff', letterSpacing: -0.5 }}>
                Nexus Trading
              </h1>
              <p style={{ margin: 0, fontSize: 12, color: '#64748b' }}>Binance Futures Testnet Engine</p>
            </div>
          </div>
          <StatusBadge status={status} />
        </div>

        {/* Main grid */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: 16, flex: 1 }}>

          {/* Left panel — API status */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <div className="glass-panel">
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
                <Activity size={18} color="#00f0ff" />
                <h2 style={{ margin: 0, fontSize: 15, fontWeight: 700 }}>System Status</h2>
              </div>
              {[
                { label: 'API', value: status === 'connected' ? 'Online' : 'Offline', ok: status === 'connected' },
                { label: 'Testnet', value: 'Active', ok: true },
                { label: 'Mode', value: 'USDT-M Futures', ok: true },
              ].map(({ label, value, ok }) => (
                <div key={label} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
                  <span style={{ fontSize: 13, color: '#94a3b8' }}>{label}</span>
                  <span style={{ fontSize: 13, fontWeight: 700, color: ok ? '#00f0ff' : '#ff003c', fontFamily: 'monospace' }}>{value}</span>
                </div>
              ))}
            </div>

            <div className="glass-panel">
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
                <Zap size={18} color="#f59e0b" />
                <h2 style={{ margin: 0, fontSize: 15, fontWeight: 700 }}>Quick Pairs</h2>
              </div>
              {['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT'].map(s => (
                <button key={s} onClick={() => setSymbol(s)} style={{
                  display: 'block', width: '100%', marginBottom: 6,
                  background: symbol === s ? 'rgba(0,240,255,0.15)' : 'rgba(255,255,255,0.03)',
                  border: `1px solid ${symbol === s ? '#00f0ff' : 'rgba(255,255,255,0.08)'}`,
                  borderRadius: 6, padding: '8px 12px', color: symbol === s ? '#00f0ff' : '#94a3b8',
                  fontSize: 13, fontWeight: 600, cursor: 'pointer', textAlign: 'left', transition: 'all 0.2s',
                }}>{s}</button>
              ))}
            </div>
          </div>

          {/* Right panel — Trade form */}
          <div className="glass-panel">
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 24 }}>
              <DollarSign size={22} color="#00f0ff" />
              <h2 style={{ margin: 0, fontSize: 18, fontWeight: 800 }}>Execute Trade</h2>
            </div>

            <form onSubmit={handleTrade} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
                <Field label="Symbol">
                  <input style={inputStyle} value={symbol} onChange={e => setSymbol(e.target.value.toUpperCase())} />
                </Field>
                <Field label="Order Type">
                  <select style={inputStyle} value={orderType} onChange={e => setOrderType(e.target.value)}>
                    <option value="MARKET">MARKET</option>
                    <option value="LIMIT">LIMIT</option>
                    <option value="STOP">STOP</option>
                  </select>
                </Field>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
                <Field label="Quantity">
                  <input style={inputStyle} type="number" step="0.001" min="0.001" value={quantity} onChange={e => setQuantity(e.target.value)} />
                </Field>
                {orderType !== 'MARKET' && (
                  <Field label="Price (USDT)">
                    <input style={inputStyle} type="number" step="0.1" min="0" value={price} onChange={e => setPrice(e.target.value)} />
                  </Field>
                )}
                {orderType === 'STOP' && (
                  <Field label="Stop Price (USDT)">
                    <input style={inputStyle} type="number" step="0.1" min="0" value={stopPrice} onChange={e => setStopPrice(e.target.value)} />
                  </Field>
                )}
              </div>

              {/* BUY / SELL toggle */}
              <div style={{ display: 'flex', gap: 0, borderRadius: 10, overflow: 'hidden', border: '1px solid rgba(255,255,255,0.1)' }}>
                {(['BUY', 'SELL'] as const).map(s => (
                  <button key={s} type="button" onClick={() => setSide(s)} style={{
                    flex: 1, padding: '12px', fontWeight: 800, fontSize: 14,
                    border: 'none', cursor: 'pointer', transition: 'all 0.2s',
                    background: side === s
                      ? s === 'BUY' ? 'linear-gradient(135deg,#00f0ff,#0055ff)' : 'linear-gradient(135deg,#ff003c,#ff6b00)'
                      : 'rgba(0,0,0,0.3)',
                    color: side === s ? 'white' : '#64748b',
                  }}>{s}</button>
                ))}
              </div>

              <button type="submit" disabled={loading} style={{
                padding: '14px', borderRadius: 10, fontWeight: 800, fontSize: 15,
                border: 'none', cursor: loading ? 'not-allowed' : 'pointer',
                background: loading ? 'rgba(255,255,255,0.1)' : btnGradient,
                color: 'white', transition: 'all 0.3s',
                boxShadow: loading ? 'none' : isBuy ? '0 0 24px rgba(0,240,255,0.35)' : '0 0 24px rgba(255,0,60,0.35)',
              }}>
                {loading ? '⏳ Executing...' : `🚀 PLACE ${side} ORDER`}
              </button>
            </form>

            {response && (
              <div style={{
                marginTop: 20, padding: '14px 16px', borderRadius: 10,
                background: response.success ? 'rgba(0,240,255,0.08)' : 'rgba(255,0,60,0.08)',
                border: `1px solid ${response.success ? '#00f0ff' : '#ff003c'}`,
                fontSize: 13, fontFamily: 'monospace', color: response.success ? '#00f0ff' : '#ff003c',
              }}>
                {response.msg}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
