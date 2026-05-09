# SCALL y Riego Automatizado para Cultivo de Café - Naranjo, Costa Rica

**Sistema de Captación de Agua de Lluvias (SCALL) + Riego Automatizado con PLC**  
**Trabajo Final de Graduación (TFG) - 2026**


---

## Descripción del Proyecto

Diseño de un **sistema piloto de riego automatizado** que aprovecha el agua de lluvia para una finca de café en **Cirri Sur, Naranjo, Alajuela**.

El sistema integra:
- **Captación inteligente de agua de lluvia** (SCALL)
- **Modelado hidrológico y balance hídrico** estocástico
- **Simulación de batería de tanques** con autonomía
- **Control automático mediante PLC** con interfaz HMI
- **Análisis técnico-económico** (VAN, TIR, CAPEX-OPEX)

El objetivo es mitigar el impacto de la irregularidad de las precipitaciones (fenómeno de El Niño, sequías) en la etapa crítica de floración y maduración del café, mejorando la productividad y la sostenibilidad hídrica.

---


## Características Principales

- Modelado hidrológico con datos históricos del IMN
- Generación de escenarios estocásticos de precipitación
- Simulación diaria de balance hídrico y comportamiento del tanque
- Análisis de rachas de sequía y autonomía del sistema
- Cálculo de eficiencia de captación y escorrentía
- Preparado para integración con automatización industrial


---

## Libreri'as necesarias

Core - Análisis de datos
- pandas>=2.2.0

Visualización y gráficos
- matplotlib>=3.8.0
- seaborn>=0.13.0

Soporte numérico
- numpy>=1.26.0

Opcionales pero recomendados
- jupyter>=1.0.0
- ipykernel>=6.29.0

Para mejor manejo de fechas y series temporales
- python-dateutil>=2.9.0
