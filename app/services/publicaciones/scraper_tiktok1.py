from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json
import time

class TikTokScraper:
    def __init__(self, headless=True):
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument('--headless=new')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')        
        chrome_options.add_argument('--disable-notifications')
        
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
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
            likes = self._find_likes_tiktok()
            comments = self._find_comments_tiktok()
            saves = self._find_saves_tiktok()
            shares = self._find_shares_tiktok()
            
            result = {
                'url': url,
                'likes': likes,
                'comments': comments,
                'saves': saves,
                'shares': shares,
                'status': 'success',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return result
            
        except Exception as e:
            return {
                'url': url,
                'likes': 0,
                'comments': 0,
                'shares': 0,
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

    
    def _find_likes_tiktok(self) -> int:
        """Extrae likes con el nuevo DOM de TikTok usando <strong data-e2e='like-count'>."""
        print("\n BUSCANDO LIKES (Nuevo DOM TikTok)...")

        try:
            strong = self.driver.find_element(
                By.XPATH,
                "//strong[@data-e2e='like-count']"
            )

            raw = strong.text.strip()  # Ej: "219", "1.3K", "2.5M"
            print(f"   🔍 Texto encontrado en <strong>: {raw}")

            number = self._convert_tiktok_number(raw)

            print(f"   ✅ Likes extraídos: {number}")
            return number

        except Exception as e:
            print(f"   ❌ Error extrayendo likes: {e}")

        return 0


    def _convert_tiktok_number(self, value: str) -> int:
        value = value.upper().replace(",", "").strip()

        if value.endswith("K"):
            return int(float(value[:-1]) * 1000)
        if value.endswith("M"):
            return int(float(value[:-1]) * 1_000_000)

        return int(float(value))

    
    def _find_saves_tiktok(self) -> int:
        """Extrae la cantidad de guardados (Favoritos) usando el nuevo DOM de TikTok."""
        print("\n💾 BUSCANDO GUARDADOS (Nuevo DOM TikTok)...")

        try:
            strong = self.driver.find_element(
                By.XPATH,
                "//strong[@data-e2e='undefined-count']"
            )

            raw = strong.text.strip()  # Ej: "148", "1.2K", "3M"
            print(f"   🔍 Texto encontrado en <strong>: {raw}")

            number = self._convert_tiktok_number(raw)

            print(f"   ✅ Guardados extraídos: {number}")
            return number

        except Exception as e:
            print(f"   ❌ Error extrayendo guardados: {e}")

        return 0


    
    
    def _find_comments_tiktok(self) -> int:
        """Extrae comentarios con el nuevo DOM de TikTok usando <strong data-e2e='comment-count'>."""
        print("\n💬 BUSCANDO COMENTARIOS (Nuevo DOM TikTok)...")

        try:
            strong = self.driver.find_element(
                By.XPATH,
                "//strong[@data-e2e='comment-count']"
            )

            raw = strong.text.strip()  # Ej: "21", "1.3K", "2.5M"
            print(f"   🔍 Texto encontrado en <strong>: {raw}")

            number = self._convert_tiktok_number(raw)

            print(f"   ✅ Comentarios extraídos: {number}")
            return number

        except Exception as e:
            print(f"   ❌ Error extrayendo comentarios: {e}")

        return 0

     
    
    def _find_shares_tiktok(self) -> int:
        """Extrae la cantidad de compartidos usando el nuevo DOM de TikTok."""
        print("\n🔗 BUSCANDO COMPARTIDOS (Nuevo DOM TikTok)...")

        try:
            strong = self.driver.find_element(
                By.XPATH,
                "//strong[@data-e2e='share-count']"
            )

            raw = strong.text.strip()  # Ej: "21", "1.2K", "3M"
            print(f"   🔍 Texto encontrado en <strong>: {raw}")

            number = self._convert_tiktok_number(raw)

            print(f"   ✅ Compartidos extraídos: {number}")
            return number

        except Exception as e:
            print(f"   ❌ Error extrayendo compartidos: {e}")

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


    def get_metrics(self, url: str) -> dict:
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
        print("🎯 INICIANDO EXTRACCIÓN FACEBOOK EN UNA SOLA VENTANA")
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
            
            if result.get('likes') == 0 or result.get('comments') == 0:
                print("\n⚠️ Algunas métricas son cero. Verifica la URL o el estado de la sesión.")
                
            self.close()
            
            return result
            
        except Exception as e:
            # Propaga cualquier error específico ocurrido durante la extracción
            raise Exception(f"Error durante la extracción de datos: {e}")  