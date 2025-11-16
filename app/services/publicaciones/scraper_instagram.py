from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json
import time

class InstagramScraper:
    def __init__(self, headless=True):
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument('--headless=new')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        chrome_options.add_argument('--window-size=400,700')
        chrome_options.add_argument('--disable-notifications')
        
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.set_window_size(400, 700)
    
    def extract_all_metrics_single_page_instagram(self, url: str) -> dict:
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
            likes = self._find_likes_instagram()
            comments = self._find_comments_instagram()
            
            # También podemos extraer otras métricas si están disponibles
            shares = self._find_shares()
            
            result = {
                'url': url,
                'likes': likes,
                'comments': comments,
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
    
    def _find_likes_instagram(self) -> int:
        """Busca likes en la vista actual"""
        print("\n❤️  BUSCANDO LIKES...")
        
        # Estrategia 1: Buscar por texto "Me gusta"
        try:
            elements_with_likes = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Me gusta')]")
            print(f"   Encontrados {len(elements_with_likes)} elementos con 'Me gusta'")
            
            for i, element in enumerate(elements_with_likes):
                try:
                    full_text = element.text
                    if full_text.strip():  # Solo si tiene texto
                        print(f"   Elemento {i+1}: '{full_text}'")
                        
                        match = re.search(r'(\d+[\d,]*)\s*Me gusta', full_text)
                        if match:
                            likes_str = match.group(1).replace(',', '')
                            print(f"   ✅ LIKES ENCONTRADOS: {likes_str}")
                            return int(likes_str)
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"   Error en búsqueda de likes: {e}")
        
        # Estrategia 2: Buscar elementos con clases específicas de likes
        try:
            like_selectors = [
                "//span[contains(@class, 'x193iq5w')]",
                "//div[contains(@class, 'like')]",
                "//a[contains(@class, 'like')]"
            ]
            
            for selector in like_selectors:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements:
                    text = element.text
                    if 'Me gusta' in text:
                        numbers = re.findall(r'\d+', text)
                        if numbers:
                            print(f"   ✅ LIKES ENCONTRADOS: {numbers[0]}")
                            return int(numbers[0])
                            
        except Exception as e:
            print(f"   Error en búsqueda alternativa de likes: {e}")
        
        print("   ❌ No se encontraron likes")
        return 0
    
    
    def _find_comments_instagram(self) -> int:
        """Busca comentarios en la vista actual"""
        print("\n💬 BUSCANDO COMENTARIOS...")
        
        # Estrategia 1: Buscar por texto "comentarios"
        try:
            elements_with_comments = self.driver.find_elements(By.XPATH, 
                "//*[contains(text(), 'comentarios') or contains(text(), 'comentario')]")
            print(f"   Encontrados {len(elements_with_comments)} elementos con 'comentarios'")
            
            for i, element in enumerate(elements_with_comments):
                try:
                    full_text = element.text
                    if full_text.strip():
                        print(f"   Elemento {i+1}: '{full_text}'")
                        
                        # Buscar "Ver los X comentarios" o "X comentarios"
                        match = re.search(r'(\d+[\d,]*)\s*comentarios', full_text, re.IGNORECASE)
                        if match:
                            comments_str = match.group(1).replace(',', '')
                            print(f"   ✅ COMENTARIOS ENCONTRADOS: {comments_str}")
                            return int(comments_str)
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"   Error en búsqueda de comentarios: {e}")
        
        # Estrategia 2: Buscar por clases específicas de comentarios
        try:
            comment_selectors = [
                "//span[contains(@class, 'x1lliihq')]",
                "//span[contains(@class, 'x1plvlek')]",
                "//a[contains(@class, 'comment')]",
                "//div[contains(@class, 'comment')]"
            ]
            
            for selector in comment_selectors:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements:
                    text = element.text
                    if 'comentario' in text.lower():
                        numbers = re.findall(r'\d+', text)
                        if numbers:
                            print(f"   ✅ COMENTARIOS ENCONTRADOS: {numbers[0]}")
                            return int(numbers[0])
                            
        except Exception as e:
            print(f"   Error en búsqueda alternativa de comentarios: {e}")
        
        print("   ❌ No se encontraron comentarios")
        return 0
     
    
    def _find_shares(self) -> int:
        """Busca shares en la vista actual (si están disponibles)"""
        print("\n🔄 BUSCANDO SHARES...")
        
        try:
            elements_with_shares = self.driver.find_elements(By.XPATH,
                "//*[contains(text(), 'compartido') or contains(text(), 'compartir') or contains(text(), 'share')]")
            
            for element in elements_with_shares:
                text = element.text
                match = re.search(r'(\d+[\d,]*)\s*(?:compartido|compartir|share)', text, re.IGNORECASE)
                if match:
                    shares_str = match.group(1).replace(',', '')
                    print(f"   ✅ SHARES ENCONTRADOS: {shares_str}")
                    return int(shares_str)
                    
        except Exception as e:
            print(f"   Error en búsqueda de shares: {e}")
        
        print("   ❌ No se encontraron shares")
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
            result = self.extract_all_metrics_single_page_instagram(url)
            
            # 3. Mostrar y verificar resultados
            print("\n" + "="*60)
            print("📊 RESULTADOS OBTENIDOS")
            print("="*60)
            
            json_result = json.dumps(result, indent=2, ensure_ascii=False)
            print(json_result)
            
            if result.get('likes') == 0 or result.get('comments') == 0:
                print("\n⚠️ Algunas métricas son cero. Verifica la URL o el estado de la sesión.")
            
            return result
            
        except Exception as e:
            # Propaga cualquier error específico ocurrido durante la extracción
            raise Exception(f"Error durante la extracción de datos: {e}")  