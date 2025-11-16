from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

class ProfileTikTokScraper:
    def __init__(self, headless=True):
        edge_options = EdgeOptions()

        # Modo headless (ocultar navegador)
        if headless:
            edge_options.add_argument("--headless=new")

        # Configuraciones recomendadas
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--disable-infobars")
        edge_options.add_argument("--disable-extensions")
        edge_options.add_argument("--window-size=1920,1080")
        edge_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        # Crear webdriver de Edge
        service = EdgeService()  # usa el edgedriver del PATH
        self.driver = webdriver.Edge(service=service, options=edge_options)

        self.wait = WebDriverWait(self.driver, 15)
    
    def extract_all_metrics_single_page_tiktok(self, url: str) -> dict:
        """
        Extrae TODAS las métricas (likes y comentarios) en una sola carga de página
        usando la misma ventana y vista
        """
        try:
            print(f"🚀 Navegando a: {url}")
            print("📊 Extrayendo TODAS las métricas en una sola ejecución...")
            
            # Solo una carga de página
            self.driver.get(url)
            time.sleep(5)
            
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Captura inicial
            self.take_screenshot("pagina_cargada.png")
            print("✅ Página cargada correctamente")
            
            # Hacer scroll para asegurar que todos los elementos estén visibles
            # print("🔄 Haciendo scroll para cargar contenido...")
            # self._smart_scroll()
            
            # Captura después del scroll
            # self.take_screenshot("despues_scroll.png")
            
            # Extraer TODAS las métricas de la misma vista
            print("\n🔍 Extrayendo métricas de la misma vista...")
            followers = self._find_followers()
            likes = self._find_profile_likes()
            
            result = {
                'url': url,
                'likes': likes,
                'followers': followers,
                'status': 'success',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return result
            
        except Exception as e:
            return {
                'url': url,
                'likes': 0,
                'followers': 0,
                'status': 'error',
                'error_message': str(e)
            }
    
    def _smart_scroll(self):
        """Hace scroll inteligente para cargar contenido"""
        scroll_positions = [100, 200, 300, 400, 500]
        
        for position in scroll_positions:
            self.driver.execute_script(f"window.scrollTo(0, {position});")
            print(f"   Scroll a {position}px")
            time.sleep(1)
        
        # Scroll adicional si es necesario
        time.sleep(2)
    
    
    def _find_followers(self) -> int:
        """
        Extrae el número de seguidores de un perfil TikTok
        Soporta valores como: 123, 4.5K, 1.2M
        """
        print("\n👥 BUSCANDO SEGUIDORES...")

        try:
            # Buscar el elemento que contiene el conteo
            element = self.driver.find_element(
                By.XPATH,
                "//strong[@data-e2e='followers-count']"
            )

            raw = element.text.strip()
            print(f"   Valor encontrado: {raw}")

            # return self._convert_tiktok_number(raw)
            return raw

        except Exception as e:
            print(f"   ❌ No se pudieron obtener los seguidores: {e}")
            return 0


    def _convert_tiktok_number(self, value: str) -> int:
        """
        Convierte valores como:
        - '16.6K' → 16600
        - '1.2M'  → 1200000
        - '850'   → 850
        """
        try:
            value = value.lower().replace(",", "").strip()

            if value.endswith("k"):
                return int(float(value[:-1]) * 1000)

            if value.endswith("m"):
                return int(float(value[:-1]) * 1_000_000)

            if value.endswith("b"):
                return int(float(value[:-1]) * 1_000_000_000)

            return int(float(value))

        except:
            return 0

    
    def _find_profile_likes(self) -> int:
        """
        Extrae el número total de 'Me gusta' del perfil de TikTok.
        Soporta valores como 123, 4.5K, 1.2M, etc.
        """
        print("\n❤️ BUSCANDO ME GUSTA DEL PERFIL...")

        try:
            element = self.driver.find_element(
                By.XPATH,
                "//strong[@data-e2e='likes-count']"
            )

            raw = element.text.strip()
            print(f"   Valor encontrado: {raw}")

            # return self._convert_tiktok_number(raw)
            return raw

        except Exception as e:
            print(f"   ❌ No se pudieron obtener los 'Me gusta': {e}")
            return 0

    
    def analyze_page_content(self):
        """Función de análisis para debugging - muestra qué elementos hay en la página"""
        print("\n🔍 ANALIZANDO CONTENIDO DE LA PÁGINA...")
        
        # Buscar todos los elementos con texto
        elements_with_text = self.driver.find_elements(By.XPATH, "//*[text() != '']")
        
        print(f"Elementos con texto encontrados: {len(elements_with_text)}")
        
        # Mostrar los primeros 20 elementos con texto relevante
        for i, element in enumerate(elements_with_text[:20]):
            text = element.text.strip()
            if text and len(text) < 100:  # Filtrar texto muy largo
                print(f"  {i+1}: '{text}'")
    
    def take_screenshot(self, filename: str = "debug.png"):
        """Toma una captura de pantalla"""
        try:
            self.driver.save_screenshot(filename)
            print(f"   📸 Captura guardada: {filename}")
        except Exception as e:
            print(f"   Error en captura: {e}")
    
    def keep_browser_open(self):
        """Mantiene el navegador abierto"""
        print("\n" + "="*60)
        print("🖥️  NAVEGADOR MANTENIDO ABIERTO")
        print("Presiona ENTER en la consola para cerrar...")
        print("="*60)
        input()
    
    def close(self):
        """Cierra el navegador"""
        print("👋 Cerrando navegador...")
        self.driver.quit()

    
    def get_profile(self, url: str) -> dict:
        """
        Realiza la extracción completa de métricas de una URL de perfil de Facebook 
        en una sola ventana/sesión.

        Args:
            url (str): La URL del perfil o página de Facebook a scrapear.

        Returns:
            dict: Un diccionario con todas las métricas extraídas.
        
        Raises:
            ValueError: Si la URL no tiene el formato correcto.
            Exception: Cualquier error que ocurra durante la extracción de datos.
        """
        print("\n" + "="*60)
        print("🎯 INICIANDO EXTRACCIÓN PROFILE FACEBOOK EN UNA SOLA VENTANA")
        print(f"🌐 URL: {url}")
        print("="*60)

        # 1. Validación de URL
        if not url.startswith(('http://', 'https://')):
            raise ValueError("❌ URL debe comenzar con http:// o https://")

        try:
            # 2. Llamada al método de extracción central (simulado)
            # ¡SOLO UNA LLAMADA! Extrae todo en la misma página
            result = self.extract_all_metrics_single_page_tiktok(url)
            
            # 3. Mostrar y verificar resultados
            print("\n" + "="*60)
            print("📊 RESULTADOS OBTENIDOS")
            print("="*60)
            
            json_result = json.dumps(result, indent=2, ensure_ascii=False)
            print(json_result)
            
            if result.get('followers') == 0:
                print("\n⚠️ Algunas métricas son cero. Verifica la URL o el estado de la sesión.")
            
            self.close()
            
            return result
            
        except Exception as e:
            # Propaga cualquier error específico ocurrido durante la extracción
            raise Exception(f"Error durante la extracción de datos: {e}")        