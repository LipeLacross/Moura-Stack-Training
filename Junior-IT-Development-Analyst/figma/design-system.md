# Design System - Moura TI

## Cores

### Primárias
```css
--primary: #1a56db;       /* Azul Moura */
--primary-dark: #1243af;
--primary-light: #3b82f6;
```

### Neutras
```css
--bg: #f8fafc;
--surface: #ffffff;
--text: #1e293b;
--text-secondary: #64748b;
--border: #e2e8f0;
```

### Semânticas
```css
--success: #22c55e;
--warning: #f59e0b;
--danger: #ef4444;
--info: #3b82f6;
```

## Tipografia

### Fontes
- **Títulos:** Inter (sans-serif)
- **Corpo:** Inter (sans-serif)
- **Código:** JetBrains Mono (monospace)

### Tamanhos
```css
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
```

## Componentes

### Cards
```css
.card {
  background: var(--surface);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  border: 1px solid var(--border);
}
```

### Botões
```css
.btn-primary {
  background: var(--primary);
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  font-weight: 500;
  cursor: pointer;
}

.btn-outline {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text);
  padding: 8px 16px;
  border-radius: 8px;
}
```

### Inputs
```css
.input {
  padding: 10px 14px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--surface);
  width: 100%;
}
```

### KPIs
```css
.kpi-card {
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  color: white;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
}
```

## Grid
- **Layout:** 12 colunas
- **Gutter:** 24px
- **Breakpoints:**
  - Mobile: 640px
  - Tablet: 768px
  - Desktop: 1024px
  - Wide: 1280px

## Exemplo no Figma
```
📁 Moura TI Design System
  ├── 🎨 Cores
  ├── 🔤 Tipografia
  ├── 🧩 Componentes
  │   ├── Cards
  │   ├── Botões
  │   ├── Inputs
  │   └── KPIs
  ├── 📐 Grid
  └── 📄 Templates
      ├── Dashboard
      └── Login
```
