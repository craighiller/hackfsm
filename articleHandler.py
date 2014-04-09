import webapp2
from helper import xmlToHTML

class ArticleHandler(webapp2.RequestHandler):
    def get(self):
        myId = escapeAndFixId(self.request.get("id"))
        info = eval(find(myId))["response"]["docs"][0] # get the first doc (should only be one)
        del info['id'] # don't display id
        template_values = {}
        if "fsmImageUrl" in info:
            image_link = info["fsmImageUrl"][-1]
            del info['fsmImageUrl']
            template_values['picture_link'] = image_link
        else:
            teiUrl = info["fsmTeiUrl"][-1]
            r = urlfetch.fetch(teiUrl).content
            xml = et.fromstring(r)
            text = xml.findall("text")[0]
            tei_to_html_tags = {}
            tei_to_html_tags["item"] = "li"
            tei_to_html_tags["list"] = "ol"
            tei_to_html_tags["pb"] = "br"

            template_values['content'] = xmlToHTML(text)
        template_values['results'] = info
        template = jinja_environment.get_template("article.html")
        self.response.out.write(template.render(template_values))