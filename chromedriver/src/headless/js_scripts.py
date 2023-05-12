def get_mime_type(uri):
  js = """
  const checkStatus = (response) => {{
    if (!response.ok) {{
      throw new Error(`HTTP ${{response.status}} - ${{response.statusText}}`);
    }}
    return response;
  }}         

  //return imgData.data
  const callback = arguments[arguments.length - 1]

  return fetch("{}")
    .then((response) => checkStatus(response) && response.blob())
    .then((blob) => callback(blob.type));
  """.format(uri)

  return js


def convert_img_to_bytes(uri):
  js = """
  const checkStatus = (response) => {{
    if (!response.ok) {{
      throw new Error(`HTTP ${{response.status}} - ${{response.statusText}}`);
    }}
    return response;
  }}         

  //return imgData.data
  const callback = arguments[arguments.length - 1]

  return fetch("{}")
    .then((response) => checkStatus(response) && response.arrayBuffer())
    .then((data) => callback(new Uint8Array(data)));
  """.format(uri)

  return js
