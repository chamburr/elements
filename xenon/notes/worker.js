const DOMAIN = "notes.chamburr.com";
const LANG = "en";
const HOME_URL = `https://www.craft.do/s/vPB5VHJ4Vvl9lV`;
const FAVICON_URL = "https://chamburr.com/favicon.ico";

addEventListener("fetch", (event) => {
  event.respondWith(fetchAndApply(event.request));
});

async function fetchAndApply(request) {
  let url = new URL(request.url);
  url.host = "www.craft.do";
  let pathname = url.pathname;
  let response = null;

  if (pathname.startsWith("/api/log/")) {
    return new Response("Logging disabled.");
  }

  if (pathname.startsWith("/api/share-analytics/")) {
    return new Response("Share analytics disabled.");
  }

  if (pathname === "/") {
    url.pathname = "/s/" + HOME_URL.slice(23);
  } else if (pathname.startsWith("/b/")) {
    url.pathname = "/s/" + HOME_URL.slice(23) + pathname;
  } else if (!pathname.includes("/api/")) {
    if (pathname.includes("/x/")) {
      url.pathname = "/s/" + HOME_URL.slice(23) + pathname;
    } else if (!pathname.includes(".")) {
      url.pathname = "/404";
    }
  }

  let method = request.method;
  let request_headers = request.headers;
  let new_request_headers = new Headers(request_headers);

  new_request_headers.set("Host", url.hostname);
  new_request_headers.set("Referer", url.hostname);

  let original_response = await fetch(url.href, {
    method: method,
    headers: new_request_headers,
  });

  let response_headers = original_response.headers;
  let new_response_headers = new Headers(response_headers);
  let status = original_response.status;

  response = new Response(original_response.body, {
    status,
    headers: new_response_headers,
  });

  let text = await response.text();
  let modified_response = new Response(text, {
    status: response.status,
    statusText: response.statusText,
    headers: response.headers,
  });

  if (pathname.startsWith("/share/") || pathname.startsWith("/api/")) {
    return modified_response;
  }

  modified_response.headers.delete("Content-Security-Policy");
  return new HTMLRewriter()
    .on("body", new BodyRewriter())
    .on("head", new HeadRewriter())
    .on("html", new AttributeRewriter(pathname))
    .on("meta", new AttributeRewriter(pathname))
    .on("link", new AttributeRewriter(pathname))
    .on('meta[name="robots"]', new RemoveElement())
    .on("head>style", new RemoveElement())
    .on('script[src="https://www.craft.do/assets/js/analytics2.js"]', new RemoveElement())
    .transform(modified_response);
}

class AttributeRewriter {
  constructor(pathname) {
    this.pathname = pathname;
  }

  element(element) {
    if (element.getAttribute("property") === "og:url") {
      element.setAttribute("content", "https://" + DOMAIN + this.pathname);
    }
    if (element.getAttribute("name") === "luki:api-endpoint") {
      element.setAttribute("content", "https://" + DOMAIN + "/api/");
    }
    if (element.getAttribute("lang") === "en") {
      element.setAttribute("lang", LANG);
    }
    if (element.getAttribute("rel") === "icon") {
      element.setAttribute("href", FAVICON_URL);
    }
    if (element.getAttribute("rel") === "apple-touch-icon") {
      element.setAttribute("href", FAVICON_URL);
    }
  }
}

class RemoveElement {
  element(element) {
    element.remove();
  }
}

class BodyRewriter {
  element(element) {
    element.append(
      `
    <script>
      function updateTitleAlignment() {
        var xpath = '//div[contains(@class, "sc-iwsKbI") and text()="CHamburr Notes"]';
        var element = document.evaluate(xpath, document, null, XPathResult.ANY_TYPE, null).iterateNext();
        if (!element) setTimeout(updateTitleAlignment, 10);
        else element.parentNode.style.textAlign = 'center';
     }
     updateTitleAlignment();
    </script>
    `,
      {
        html: true,
      },
    );
  }
}

class HeadRewriter {
  element(element) {
    element.append(
      `
    <style>
      #topContainer a {
        display: none;
      }
      #topContainer .separator {
        display: none;
      }
    </style>
    `,
      {
        html: true,
      },
    );
  }
}
