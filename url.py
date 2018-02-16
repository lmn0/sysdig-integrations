from checks import AgentCheck
import urllib2
import urllib

class MyCustomCheck(AgentCheck):
    def check(self, instance):
        for urllist in instance['urllist']:
            headers = {'User-agent':'sysdig-agent'}
            url = urllist['url']
            try:
              url_data = urllist['data']
            except:
              url_data = None
            try:
              data = None
              if url_data != None:
                data = urllib.urlencode(url_data)
              req = urllib2.Request(url,data,headers)
              conn = urllib2.urlopen(req)
              status = conn.getcode()
            except urllib2.HTTPError, e:
              self.gauge("url_health", e.code, ["url:"+url])
            except urllib2.URLError, e:
              self.log.exception(str(e.error))
            else:
              self.gauge("url_health", status, ["url:"+url])
            finally:
              try:
                conn.close()
              except:
                pass
