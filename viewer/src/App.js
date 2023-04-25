import React, {useState, useEffect} from 'react'
import CodeMirror from 'react-codemirror';

import {JSONToHTMLTable} from '@kevincobain2000/json-to-html-table'


export const App = () => {
  const handleChangeData = (data) => {
    setData(data)
  }

  const [data, setData] = useState(`
  {
  "ruletype_id": "1",
  "ruletype_name": "Process Creation",
  "comment": "Temporarily disabled to see if alerting to Sentinel reduced",
  "name": "Double extension Executable",
  "description": "Double extension Executable not running in normal locations",
  "pattern_id": "41004",
  "pattern_severity": "informational",
  "action_label": "Detect",
  "disposition_id": 20,
  "field_values": [
      {
          "name": "GrandparentImageFilename",
          "value": ".*",
          "label": "Grandparent Image Filename",
          "type": "excludable",
          "values": [
              {
                  "label": "include",
                  "value": ".*"
              }
          ],
          "final_value": ".*"
      },
      {
          "name": "GrandparentCommandLine",
          "value": ".*",
          "label": "Grandparent Command Line",
          "type": "excludable",
          "values": [
              {
                  "label": "include",
                  "value": ".*"
              }
          ],
          "final_value": ".*"
      },
      {
          "name": "ParentImageFilename",
          "value": ".*",
          "label": "Parent Image Filename",
          "type": "excludable",
          "values": [
              {
                  "label": "include",
                  "value": ".*"
              }
          ],
          "final_value": ".*"
      },


      {
          "name": "CommandLine",
          "value": ".*",
          "label": "Command Line",
          "type": "excludable",
          "values": [
              {
                  "label": "include",
                  "value": ".*"
              }
          ],
          "final_value": ".*"
      }
  ]
}
`)

  useEffect(() => {
  }, [])
  const renderTable = () => {
    try {
      return <JSONToHTMLTable data={JSON.parse(data)} tableClassName="table table-condensed table-sm" />
    } catch (error) {
      return <div>Error in JSON</div>
    }
  }

  const format = (html) => {
    var tab = '  ';
    var result = '';
    var indent= '';

    html.split(/>\s*</).forEach(function(element) {
        if (element.match( /^\/\w/ )) {
            indent = indent.substring(tab.length);
        }

        result += indent + '<' + element + '>\r\n';

        if (element.match( /^<?\w[^>]*[^\/]$/ )) {
            indent += tab;
        }
    });

    return result.substring(1, result.length-3);
  }

  const options = {
    height: "70px",
    width: "100%",
    theme: "ambiance",
    lineNumbers: true,
    styleActiveLine: true,
    textWrapping: true,
    mode: "javascript",
  }

  return (
    <div className="container">
        <h1 className="text-center">
       Custom IOA JSON Viewer
      </h1>
      <p>Enter JSON</p>
      <div className='pt-2 pb-2'>
        <CodeMirror value={data} onChange={handleChangeData} options={options} />
        <br/>
        <p>HTML Table</p>
        {renderTable()}
      </div>
    </div>
  )
}
export default App;
