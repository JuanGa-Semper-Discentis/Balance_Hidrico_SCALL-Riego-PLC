# SCALL y Riego Automatizado para Cultivo de Café - Naranjo, Costa Rica

**Sistema de Captación de Agua de Lluvias (SCALL) + Riego Automatizado con PLC**  
**Trabajo Final de Graduación (TFG) - 2026**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PLC](https://img.shields.io/badge/PLC-Automation-FF6600?style=for-the-badge)
![Costa Rica](https://img.shields.io/badge/Costa%20Rica-00A86B?style=for-the-badge)

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


## Tecnologías Utilizadas

- **Python** (pandas, matplotlib, seaborn)
- **PLC** + HMI (pendiente de implementación)
- **Control hidráulico** y sensores de nivel/ultrasonido
- Análisis de series temporales y simulación Monte Carlo

---

## Resultados Destacados

- Área de captación optimizada
- Dimensionamiento de batería de tanques (4 × Ecotank Poseidon 27.000 L)
- Análisis de viabilidad económica y periodos de retorno
- Modelos validados con datos reales de Naranjo

---

## Cómo Usar

```bash
# Clonar repositorio
git clone https://github.com/tuusuario/SCALL-Riego-Automatizado-Cafe-Naranjo.git

# Instalar dependencias
cd SCALL-Riego-Automatizado-Cafe-Naranjo
pip install -r requirements.txt

# Ejecutar simulaciones
python src/python/8-Balance_Hidrico_ext.py
python src/python/9-Graficar_B_Hidrico.py
python src/python/10-Simulacion_Tanque.py
