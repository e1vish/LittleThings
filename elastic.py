import os
import lxml
from requests import request
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"
}

elasticbeats = {
    "auditbeat": "https://www.elastic.co/downloads/beats/auditbeat",
    "filebeat": "https://www.elastic.co/downloads/beats/filebeat",
    "functionbeat": "https://www.elastic.co/downloads/beats/functionbeat",
    "heartbeat": "https://www.elastic.co/downloads/beats/heartbeat",
    "journalbeat": "https://www.elastic.co/downloads/beats/filebeat",
    "metricbeat": "https://www.elastic.co/downloads/beats/metricbeat",
    "packetbeat": "https://www.elastic.co/downloads/beats/packetbeat",
    "winlogbeat": "https://www.elastic.co/downloads/beats/winlogbeat"
}

elasticstack = {
    "elasticsearch": "https://www.elastic.co/downloads/elasticsearch",
    "logstash": "https://www.elastic.co/downloads/logstash",
    "kibana": "https://www.elastic.co/downloads/kibana",
    "apm-server": "https://www.elastic.co/downloads/apm",
    "app-search": "https://www.elastic.co/downloads/app-search"
}

grafanalabs = {
    "grafana-linux": "https://grafana.com/grafana/download?platform=linux",
    "grafana-windows": "https://grafana.com/grafana/download?platform=windows",
    "grafana-source": "https://github.com/grafana/grafana/releases",
    "cortex": "https://github.com/cortexproject/cortex/releases",
    "graphite": "https://github.com/graphite-project/graphite-web/releases",
    "loki": "https://github.com/grafana/loki/releases",
    "metrictank": "https://github.com/grafana/metrictank/releases"
}

prometheus = {
    "prometheus": "https://github.com/prometheus/prometheus/releases",
    "alertmanager": "https://github.com/prometheus/alertmanager/releases",
    "blackbox_exporter": "https://github.com/prometheus/blackbox_exporter/releases",
    "cloudwatch_exporter": "https://github.com/prometheus/cloudwatch_exporter",
    "consul_exporter": "https://github.com/prometheus/consul_exporter/releases",
    "graphite_exporter": "https://github.com/prometheus/graphite_exporter/releases",
    "haproxy_exporter": "https://github.com/prometheus/haproxy_exporter/releases",
    "influxdb_exporter": "https://github.com/prometheus/influxdb_exporter/releases",
    "jmx_exporter": "https://github.com/prometheus/jmx_exporter/releases",
    "memcached_exporter": "https://github.com/prometheus/memcached_exporter/releases",
    "mysqld_exporter": "https://github.com/prometheus/mysqld_exporter/releases",
    "node_exporter": "https://github.com/prometheus/node_exporter/releases",
    "pushgateway": "https://github.com/prometheus/pushgateway/releases",
    "snmp_exporter": "https://github.com/prometheus/snmp_exporter/releases",
    "statsd_exporter": "https://github.com/prometheus/statsd_exporter/releases"
}


def get_soup(url):
    response = request('GET', url, headers=headers)
    response.encoding = 'UTF-8'
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    return soup


def get_from_classname(url, classname):
    links = []
    if url:
        soup = get_soup(url)
    items = soup.find_all(class_=classname)
    if items:
        lists = items[0].find_all('li')
        for i in range(len(lists)):
            ahrefs = lists[i].find_all('a')
            arch = ahrefs[0].text
            if "32-bit" in arch or "beta" in arch:
                pass
            else:
                for j in range(len(ahrefs)):
                    link = ahrefs[j].get('href')
                    links.append(link)
    return links


def get_file(urls, dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    if urls:
        for url in urls:
            filename = url.split('/')[-1]
            response = request('GET', url, stream=True, headers=headers)
            with open(dir + '/' + filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
            print(filename + ' download successfully.')
    return None


def get_elastic(elastic):
    classname = "jsx-1465493893 downloads"
    for key in elastic:
        urls = get_from_classname(elastic[key], classname)
        get_file(urls, key)
    return None


def main():
    get_elastic(elasticbeats)
    get_elastic(elasticstack)


if __name__ == "__main__":
    main()