class LlmParser:
    def __init__(self, format='JSON') -> None:
        if format == 'JSON':
            self.format = format
            self._formatter = JSONParser()
        else:
            raise NotImplementedError(f"Format type \"{format}\" not implemented yet.")
    
    def parse(self, llm_response):
        return self._formatter.parse(llm_response)

    def parse_with_keys(self, llm_response, expected_keys):
        parsed_json = self.parse(llm_response)
        real_json = parsed_json['json']
        missing_keys = [key for key in expected_keys if key not in real_json.keys()]
        print(missing_keys)
        print(missing_keys)
        print(missing_keys)
        if missing_keys:
            parsed_json['state'] = 'MISSING_KEYS'
        return parsed_json

# -----------------------------------------------------------------------------------------
import json
from json.decoder import JSONDecodeError
import re
class JSONParser():
    
    def _handle_bad_answer(self, llm_response):
        possible_jsons = re.findall(r'\{.*?\}', llm_response)
        for fragment in possible_jsons:
            try:
                return json.loads(fragment), 'ERROR_EXTRA_TEXT'
            except:
                continue
        return {}, 'ERROR_INVALID_JSON'

    def parse(self, llm_response):
        try:
            json_llm = json.loads(llm_response)
            state = 'VALID'
        except JSONDecodeError as e:
            json_llm, state = self._handle_bad_answer(llm_response)
        final_json = {}
        final_json['json'] = json_llm
        final_json['state'] = state
        return final_json