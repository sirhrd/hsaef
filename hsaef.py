import socket
import ssl
import urllib.request
import re
import time
import json
from urllib.parse import urlparse
from datetime import datetime

LOGO = """
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠈⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣄⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠾⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⣤⣶⣤⣉⣿⣿⡯⣀⣴⣿⡗⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⡈⠀⠀⠉⣿⣿⣶⡉⠀⠀⣀⡀⠀⠀⠀⢻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠉⢉⣽⣿⠿⣿⡿⢻⣯⡍⢁⠄⠀⠀⠀⣸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠐⡀⢉⠉⠀⠠⠀⢉⣉⠀⡜⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠿⠁⠀⠀⠀⠘⣤⣭⣟⠛⠛⣉⣁⡜⠀⠀⠀⠀⠀⠛⠿⣿⣿⣿
⡿⠟⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⡀⠀⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀
  By @HRD Tools hsaef-حسايف
"""

def get_site_info(url):
    """"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path.split('/')[0]
        
        info = {
            '1. الموقع': url,
            '2. النطاق': domain,
            '3. البروتوكول': parsed.scheme if parsed.scheme else 'غير محدد',
            '4. المسار': parsed.path if parsed.path else '/',
            '5. الاستعلام': parsed.query if parsed.query else 'لا يوجد',
            '6. المعلمات': parsed.params if parsed.params else 'لا يوجد'
        }
        
        try:
            ip = socket.gethostbyname(domain)
            info['7. عنوان IP'] = ip
            info['8. موقع الخادم'] = get_server_location(ip)
            info['9. مزود الخدمة'] = get_isp_info(ip)
            
            # معلومات إضافية عن IP
            try:
                hostname, aliases, addresses = socket.gethostbyaddr(ip)
                info['10. اسم المضيف'] = hostname
                info['11. الأسماء المستعارة'] = ', '.join(aliases) if aliases else 'لا يوجد'
            except:
                info['10. اسم المضيف'] = 'غير متاح'
                info['11. الأسماء المستعارة'] = 'غير متاح'
                
        except:
            info['7. عنوان IP'] = 'غير متاح'
            info['8. موقع الخادم'] = 'غير متاح'
            info['9. مزود الخدمة'] = 'غير متاح'
            info['10. اسم المضيف'] = 'غير متاح'
            info['11. الأسماء المستعارة'] = 'غير متاح'
        
        ssl_info = check_ssl(domain)
        info.update(ssl_info)
        
        page_info = analyze_page(url)
        info.update(page_info)
        
        info['32. الروابط الخارجية'] = count_external_links(url)
        info['33. الروابط الداخلية'] = count_internal_links(url)
        info['34. الملفات'] = find_resources(url)
        
        headers_info = get_headers_info(url)
        info.update(headers_info)
        
        info['45. سرعة التحميل'] = measure_load_time(url)
        info['46. حالة الموقع'] = check_site_status(url)
        
        # معلومات إضافية لبلوغ 50 معلومة
        info['47. دعم HTTPS'] = 'نعم' if parsed.scheme == 'https' else 'لا'
        info['48. منفذ الخادم'] = parsed.port if parsed.port else 'افتراضي (80/443)'
        info['49. تاريخ التحليل'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        info['50. لغة البرمجة'] = detect_programming_language(page_info.get('25. التقنيات', ''))
        
        return info
        
    except Exception as e:
        return {'خطأ': str(e)}

def check_ssl(domain):
    """فحص شهادة SSL بشكل متقدم"""
    result = {}
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                result['12. حالة SSL'] = 'نشط'
                result['13. الصادر من'] = dict(x[0] for x in cert['issuer'])['organizationName']
                result['14. صالح ل'] = dict(x[0] for x in cert['subject'])['commonName']
                
                start = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                end = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                result['15. تاريخ البدء'] = start.strftime('%Y-%m-%d')
                result['16. تاريخ الانتهاء'] = end.strftime('%Y-%m-%d')
                
                remaining = (end - datetime.now()).days
                result['17. الأيام المتبقية'] = remaining
                result['18. التشفير'] = ssock.cipher()[0]
                result['19. إصدار SSL'] = ssock.version()
                result['20. قوة التشفير'] = f"{ssock.cipher()[2]} بت"
                
    except:
        result['12. حالة SSL'] = 'غير نشط'
        result['13. الصادر من'] = 'غير متاح'
        result['14. صالح ل'] = 'غير متاح'
        result['15. تاريخ البدء'] = 'غير متاح'
        result['16. تاريخ الانتهاء'] = 'غير متاح'
        result['17. الأيام المتبقية'] = 'غير متاح'
        result['18. التشفير'] = 'غير متاح'
        result['19. إصدار SSL'] = 'غير متاح'
        result['20. قوة التشفير'] = 'غير متاح'
    return result

def analyze_page(url):
    """تحليل محتوى الصفحة"""
    result = {}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            result['21. حجم الصفحة'] = f"{len(html)/1024:.1f} كيلوبايت"
            result['22. الترميز'] = response.headers.get_content_charset() or 'غير معروف'
            result['23. الاستجابة'] = response.getcode()
            
            title_match = re.search('<title>(.*?)</title>', html, re.IGNORECASE)
            result['24. العنوان'] = title_match.group(1) if title_match else 'غير موجود'
            
            desc_match = re.search('<meta name="description" content="(.*?)"', html, re.IGNORECASE)
            result['25. الوصف'] = desc_match.group(1) if desc_match else 'غير موجود'
            
            keywords_match = re.search('<meta name="keywords" content="(.*?)"', html, re.IGNORECASE)
            result['26. الكلمات المفتاحية'] = keywords_match.group(1) if keywords_match else 'غير موجود'
            
            result['27. عدد الروابط'] = len(re.findall('<a [^>]*href=', html))
            result['28. عدد الصور'] = len(re.findall('<img[^>]*src=', html))
            result['29. عدد النصوص'] = len(re.findall('<p>|<span>|<div>', html))
            result['30. عدد النماذج'] = len(re.findall('<form', html))
            
            tech = detect_technologies(html, response.headers)
            result['31. التقنيات'] = tech if tech else 'غير معروف'
            
            result['32. لغة الموقع'] = detect_language(html)
            
            # معلومات إضافية
            viewport_match = re.search('<meta name="viewport" content="(.*?)"', html, re.IGNORECASE)
            result['33. Viewport'] = viewport_match.group(1) if viewport_match else 'غير موجود'
            
            generator_match = re.search('<meta name="generator" content="(.*?)"', html, re.IGNORECASE)
            result['34. المولد'] = generator_match.group(1) if generator_match else 'غير موجود'
            
            # اكتشاف إطارات العمل
            result['35. إطارات العمل'] = detect_frameworks(html)
            
    except Exception as e:
        result['تحليل الصفحة'] = f"فشل التحليل: {str(e)}"
    return result

def detect_technologies(html, headers):
    """كشف التقنيات المستخدمة"""
    tech = []
    
    cms_signatures = {
        'WordPress': ['wp-content', 'wp-includes', 'wp-json'],
        'Joomla': ['joomla', 'Joomla!', '/media/jui/'],
        'Drupal': ['drupal', 'Drupal.settings', '/sites/all/'],
        'Magento': ['magento', '/static/version'],
        'Shopify': ['shopify', 'cdn.shopify.com'],
        'Wix': ['wix.com', 'static.parastorage.com'],
        'Squarespace': ['squarespace.com', 'static1.squarespace.com']
    }
    
    for cms, signs in cms_signatures.items():
        if any(sign in html for sign in signs):
            tech.append(cms)
            break
    
    server = headers.get('Server', '').lower()
    if 'apache' in server:
        tech.append('Apache')
    elif 'nginx' in server:
        tech.append('Nginx')
    elif 'iis' in server:
        tech.append('IIS')
    elif 'cloudflare' in server:
        tech.append('Cloudflare')
    elif 'litespeed' in server:
        tech.append('LiteSpeed')
    
    if 'php' in server or 'php' in html.lower():
        tech.append('PHP')
    elif 'asp.net' in server or 'asp.net' in html.lower():
        tech.append('ASP.NET')
    elif 'node.js' in server or 'node.js' in html.lower():
        tech.append('Node.js')
    elif 'python' in server or 'python' in html.lower():
        tech.append('Python')
    elif 'ruby' in server or 'ruby' in html.lower():
        tech.append('Ruby')
    elif 'java' in server or 'java' in html.lower():
        tech.append('Java')
    
    if 'bootstrap' in html.lower():
        tech.append('Bootstrap')
    if 'jquery' in html.lower():
        tech.append('jQuery')
    if 'react' in html.lower():
        tech.append('React')
    if 'vue' in html.lower():
        tech.append('Vue.js')
    if 'angular' in html.lower():
        tech.append('Angular')
    
    # اكتشاف خدمات الطرف الثالث
    if 'google-analytics' in html.lower():
        tech.append('Google Analytics')
    if 'gtm' in html.lower():
        tech.append('Google Tag Manager')
    if 'facebook.net' in html.lower():
        tech.append('Facebook Pixel')
    if 'recaptcha' in html.lower():
        tech.append('reCAPTCHA')
    
    return ', '.join(tech) if tech else 'غير معروف'

def detect_frameworks(html):
    """اكتشاف إطارات العمل"""
    frameworks = []
    
    framework_signatures = {
        'Laravel': ['laravel', 'csrf-token'],
        'Django': ['django', 'csrftoken'],
        'Rails': ['rails', 'csrf-token'],
        'Express': ['express'],
        'Spring': ['spring'],
        'Symfony': ['symfony']
    }
    
    for framework, signs in framework_signatures.items():
        if any(sign in html.lower() for sign in signs):
            frameworks.append(framework)
    
    return ', '.join(frameworks) if frameworks else 'غير معروف'

def detect_language(html):
    """اكتشاف لغة الموقع"""
    lang_match = re.search('<html[^>]*lang=["\']([^"\']*)["\']', html, re.IGNORECASE)
    if lang_match:
        return lang_match.group(1)
    
    # محاولة التخمين من المحتوى
    arabic_chars = re.findall('[\u0600-\u06FF]', html)
    english_chars = re.findall('[a-zA-Z]', html)
    
    if len(arabic_chars) > len(english_chars):
        return 'العربية'
    elif len(english_chars) > len(arabic_chars):
        return 'الإنجليزية'
    
    return 'غير معروف'

def detect_programming_language(tech_string):
    """اكتشاف لغة البرمجة المستخدمة"""
    if 'PHP' in tech_string:
        return 'PHP'
    elif 'ASP.NET' in tech_string:
        return 'ASP.NET'
    elif 'Node.js' in tech_string:
        return 'JavaScript (Node.js)'
    elif 'Python' in tech_string:
        return 'Python'
    elif 'Ruby' in tech_string:
        return 'Ruby'
    elif 'Java' in tech_string:
        return 'Java'
    else:
        return 'غير معروف'

def count_external_links(url):
    """عد الروابط الخارجية"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            domain = urlparse(url).netloc
            links = re.findall('<a [^>]*href="(http[s]?://.*?)"', html)
            
            external = 0
            for link in links:
                if domain not in link:
                    external += 1
            return external
    except:
        return 'غير متاح'

def count_internal_links(url):
    """عد الروابط الداخلية"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            domain = urlparse(url).netloc
            links = re.findall('<a [^>]*href="(http[s]?://.*?)"', html)
            
            internal = 0
            for link in links:
                if domain in link:
                    internal += 1
            return internal
    except:
        return 'غير متاح'

def find_resources(url):
    """اكتشاف الملفات والموارد"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            resources = {
                'CSS': len(re.findall('<link[^>]*href=".*?\.css"', html)),
                'JS': len(re.findall('<script[^>]*src=".*?\.js"', html)),
                'صور': len(re.findall('<img[^>]*src=".*?(\.jpg|\.png|\.gif|\.webp|\.svg|\.jpeg)"', html)),
                'ملفات': len(re.findall('href=".*?(\.pdf|\.doc|\.docx|\.zip|\.rar|\.txt|\.xls|\.xlsx)"', html))
            }
            return resources
    except:
        return 'غير متاح'

def get_headers_info(url):
    """استخراج معلومات من رؤوس الاستجابة"""
    result = {}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        with urllib.request.urlopen(req, timeout=15) as response:
            headers = response.headers
            
            result['36. نوع الخادم'] = headers.get('Server', 'غير معروف')
            result['37. نوع المحتوى'] = headers.get('Content-Type', 'غير معروف')
            result['38. آخر تعديل'] = headers.get('Last-Modified', 'غير معروف')
            result['39. كاش'] = headers.get('Cache-Control', 'غير معروف')
            result['40. الوقت'] = headers.get('Date', 'غير معروف')
            result['41. اتصال'] = headers.get('Connection', 'غير معروف')
            result['42. الترميز'] = headers.get('Content-Encoding', 'غير معروف')
            result['43. طول المحتوى'] = headers.get('Content-Length', 'غير معروف')
            result['44. نوع الترميز'] = headers.get('Transfer-Encoding', 'غير معروف')
            
            return result
    except:
        return {'رؤوس الاستجابة': 'غير متاحة'}

def measure_load_time(url):
    """قياس وقت تحميل الموقع"""
    try:
        import time
        start_time = time.time()
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        with urllib.request.urlopen(req, timeout=15) as response:
            response.read()
        end_time = time.time()
        load_time = (end_time - start_time) * 1000  # تحويل إلى ملي ثانية
        return f"{load_time:.2f} ملي ثانية"
    except:
        return 'غير متاح'

def check_site_status(url):
    """فحص حالة الموقع"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        with urllib.request.urlopen(req, timeout=15) as response:
            status = response.getcode()
            if status == 200:
                return 'يعمل بشكل طبيعي'
            else:
                return f'يعمل مع رمز حالة: {status}'
    except urllib.error.HTTPError as e:
        return f'خطأ HTTP: {e.code}'
    except Exception as e:
        return f'خطأ: {str(e)}'

def get_server_location(ip):
    """تحديد موقع الخادم (تقريبي)"""
    if ip.startswith(('5.', '185.', '78.', '79.', '80.', '81.', '82.', '83.', '84.', '85.', '86.', '87.', '88.', '89.')):
        return 'أوروبا'
    elif ip.startswith(('8.', '12.', '13.', '23.', '24.', '45.', '50.', '63.', '64.', '65.', '66.', '67.', '68.', '69.', '70.', '71.', '72.', '73.', '74.', '75.', '76.', '96.', '97.', '98.', '99.', '104.', '107.', '108.', '152.', '162.', '172.', '173.', '174.', '184.', '192.', '198.', '199.', '204.', '205.', '206.', '207.', '208.', '209.')):
        return 'أمريكا الشمالية'
    elif ip.startswith(('41.', '102.', '105.', '154.', '156.', '160.', '164.', '165.', '196.', '197.')):
        return 'أفريقيا'
    elif ip.startswith(('1.', '14.', '27.', '36.', '39.', '42.', '43.', '49.', '58.', '59.', '60.', '61.', '101.', '103.', '106.', '110.', '111.', '112.', '113.', '114.', '115.', '116.', '117.', '118.', '119.', '120.', '121.', '122.', '123.', '124.', '125.', '126.', '150.', '163.', '171.', '175.', '180.', '182.', '183.', '202.', '203.', '210.', '211.', '218.', '219.', '220.', '221.', '222.', '223.')):
        return 'آسيا'
    elif ip.startswith(('200.', '201.')):
        return 'أمريكا الجنوبية'
    else:
        return 'غير معروف'

def get_isp_info(ip):
    """الحصول على معلومات مزود الخدمة (تقريبية)"""
    if ip.startswith(('5.', '78.', '79.', '80.', '81.', '82.', '83.', '84.', '85.', '86.', '87.', '88.', '89.')):
        return 'مزود أوروبي'
    elif ip.startswith(('8.', '12.', '13.', '23.', '24.', '45.', '50.', '63.', '64.', '65.', '66.', '67.', '68.', '69.', '70.', '71.', '72.', '73.', '74.', '75.', '76.', '96.', '97.', '98.', '99.', '104.', '107.', '108.', '152.', '162.', '172.', '173.', '174.', '184.', '192.', '198.', '199.', '204.', '205.', '206.', '207.', '208.', '209.')):
        return 'مزود أمريكي'
    elif ip.startswith(('41.', '102.', '105.', '154.', '156.', '160.', '164.', '165.', '196.', '197.')):
        return 'مزود أفريقي'
    elif ip.startswith(('1.', '14.', '27.', '36.', '39.', '42.', '43.', '49.', '58.', '59.', '60.', '61.', '101.', '103.', '106.', '110.', '111.', '112.', '113.', '114.', '115.', '116.', '117.', '118.', '119.', '120.', '121.', '122.', '123.', '124.', '125.', '126.', '150.', '163.', '171.', '175.', '180.', '182.', '183.', '202.', '203.', '210.', '211.', '218.', '219.', '220.', '221.', '222.', '223.')):
        return 'مزود آسيوي'
    elif ip.startswith(('200.', '201.')):
        return 'مزود أمريكا الجنوبية'
    else:
        return 'غير معروف'

def display_info(info):
    """عرض المعلومات بطريقة منظمة"""
    print("\n" + "="*70)
    print(f"تقرير تحليل الموقع: {info.get('1. الموقع', 'غير معروف')}")
    print("="*70)
    
    sections = {
        'المعلومات الأساسية': ['1. الموقع', '2. النطاق', '3. البروتوكول', '4. المسار', '5. الاستعلام', '6. المعلمات', '7. عنوان IP', '8. موقع الخادم', '9. مزود الخدمة', '10. اسم المضيف', '11. الأسماء المستعارة'],
        'أمان الموقع': ['12. حالة SSL', '13. الصادر من', '14. صالح ل', '15. تاريخ البدء', '16. تاريخ الانتهاء', '17. الأيام المتبقية', '18. التشفير', '19. إصدار SSL', '20. قوة التشفير'],
        'استجابة الموقع': ['23. الاستجابة', '45. سرعة التحميل', '46. حالة الموقع', '47. دعم HTTPS', '48. منفذ الخادم'],
        'تحليل المحتوى': ['24. العنوان', '25. الوصف', '26. الكلمات المفتاحية', '21. حجم الصفحة', '22. الترميز', '27. عدد الروابط', '28. عدد الصور', '29. عدد النصوص', '30. عدد النماذج', '32. لغة الموقع', '31. التقنيات', '33. Viewport', '34. المولد', '35. إطارات العمل'],
        'رؤوس الاستجابة': ['36. نوع الخادم', '37. نوع المحتوى', '38. آخر تعديل', '39. كاش', '40. الوقت', '41. اتصال', '42. الترميز', '43. طول المحتوى', '44. نوع الترميز'],
        'الموارد': ['34. الملفات'],
        'الروابط': ['32. الروابط الخارجية', '33. الروابط الداخلية'],
        'معلومات إضافية': ['49. تاريخ التحليل', '50. لغة البرمجة']
    }
    
    for section, fields in sections.items():
        print(f"\n{section}:")
        print("-" * len(section))
        for field in fields:
            value = info.get(field)
            if value:
                print(f"  - {field}: {value}")

def save_to_file(info, filename):
    """حفظ المعلومات إلى ملف"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write(f"تقرير تحليل الموقع: {info.get('1. الموقع', 'غير معروف')}\n")
            f.write("="*70 + "\n\n")
            
            for key, value in info.items():
                if not key.startswith('خطأ'):
                    f.write(f"{key}: {value}\n")
            
        print(f"\nتم حفظ التقرير في ملف: {filename}")
    except Exception as e:
        print(f"حدث خطأ أثناء حفظ الملف: {str(e)}")

def main():
    print(LOGO)
    print("")
    print("="*60)
    
    while True:
        url = input("\nأدخل رابط الموقع (أو اكتب 'خروج' للإنهاء): ").strip()
        
        if url.lower() in ['exit', 'خروج', 'quit']:
            print("تم إنهاء البرنامج. إلى اللقاء!")
            break
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        try:
            print("جاري تحليل الموقع، يرجى الانتظار...")
            site_info = get_site_info(url)
            display_info(site_info)
            
            # عرض عدد المعلومات المستخرجة
            valid_info_count = len([k for k in site_info.keys() if not k.startswith('خطأ')])
            print(f"")
            
            # خيار حفظ النتائج
            save = input("\nهل تريد حفظ النتائج في ملف؟ (نعم/لا): ").strip().lower()
            if save in ['نعم', 'yes', 'y']:
                domain = urlparse(url).netloc
                filename = f"site_report_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                save_to_file(site_info, filename)
                
        except Exception as e:
            print(f"حدث خطأ أثناء التحليل: {str(e)}")
            
        input("\nاضغط Enter لتحليل موقع آخر...")

if __name__ == "__main__":
    main()