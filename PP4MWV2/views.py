from django.http import HttpResponse
from django.views import View
import xml.etree.ElementTree as ET

# Robots.txt file
class RobotsTxtView(View):
    def get(self, request):
        lines = [
            "User-agent: *",
            "Disallow: /admin/",
            "Allow: /",
            "Sitemap: https://www.masterworks.com/sitemap.xml",
        ]
        return HttpResponse("\n".join(lines), content_type="text/plain")

class SitemapView(View):
    def get(self, request):
        urls = [
            {"loc": "https://www.masterworks.com/", "lastmod": "2024-09-10", "changefreq": "daily", "priority": "1.0"},
            {"loc": "https://www.masterworks.com/faq", "lastmod": "2024-09-09", "changefreq": "yearly", "priority": "0.5"},
            {"loc": "https://www.masterworks.com/workshop", "lastmod": "2024-09-09", "changefreq": "yearly", "priority": "0.8"},
        ]

        urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

        for url in urls:
            url_elem = ET.SubElement(urlset, "url")
            ET.SubElement(url_elem, "loc").text = url["loc"]
            ET.SubElement(url_elem, "lastmod").text = url["lastmod"]
            ET.SubElement(url_elem, "changefreq").text = url["changefreq"]
            ET.SubElement(url_elem, "priority").text = url["priority"]

        xml_str = ET.tostring(urlset, encoding="utf-8", method="xml")
        return HttpResponse(xml_str, content_type="application/xml")

