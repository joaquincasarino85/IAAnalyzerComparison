"""
Script para verificar la configuración de las API keys
"""
import os
from dotenv import load_dotenv

def check_api_keys():
    """Verifica que todas las API keys necesarias estén configuradas"""
    load_dotenv()
    
    api_keys = {
        "OPENAI_API_KEY": "ChatGPT",
        "ANTHROPIC_API_KEY": "Claude", 
        "GEMINI_API_KEY": "Gemini",
        "MISTRAL_API_KEY": "Mistral",
        "COHERE_API_KEY": "Cohere",
        "PERPLEXITY_API_KEY": "Perplexity"
    }
    
    print("🔍 Verificando configuración de API Keys...")
    print("=" * 50)
    
    available_ais = []
    missing_ais = []
    
    for env_key, ai_name in api_keys.items():
        api_key = os.getenv(env_key)
        
        if api_key and api_key.strip():
            # Verificar que no sea solo espacios o caracteres vacíos
            if len(api_key.strip()) > 10:  # API keys típicamente tienen más de 10 caracteres
                print(f"✅ {ai_name}: Configurado correctamente")
                available_ais.append(ai_name)
            else:
                print(f"❌ {ai_name}: API key muy corta o inválida")
                missing_ais.append(ai_name)
        else:
            print(f"❌ {ai_name}: API key no configurada")
            missing_ais.append(ai_name)
    
    print("=" * 50)
    print(f"📊 Resumen:")
    print(f"   IAs disponibles: {len(available_ais)}")
    print(f"   IAs faltantes: {len(missing_ais)}")
    
    if available_ais:
        print(f"   ✅ IAs listas para usar: {', '.join(available_ais)}")
    
    if missing_ais:
        print(f"   ⚠️ IAs que necesitan configuración: {', '.join(missing_ais)}")
        print("\n📝 Para configurar las API keys faltantes:")
        print("   1. Obtén las API keys de los servicios correspondientes")
        print("   2. Agrégalas al archivo .env en la raíz del proyecto")
        print("   3. Reinicia la aplicación")
    
    return available_ais, missing_ais

def get_available_ais():
    """Retorna la lista de IAs disponibles"""
    available, _ = check_api_keys()
    return available

if __name__ == "__main__":
    check_api_keys() 