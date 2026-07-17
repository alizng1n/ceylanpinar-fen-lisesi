import os
import json

log_path = r"C:\Users\Acer\.gemini\antigravity\brain\6f72dc90-862c-4327-a3db-43ee1f05bf95\.system_generated\logs\transcript_full.jsonl"
if not os.path.exists(log_path):
    # Try transcript.jsonl
    log_path = r"C:\Users\Acer\.gemini\antigravity\brain\6f72dc90-862c-4327-a3db-43ee1f05bf95\.system_generated\logs\transcript.jsonl"
    if not os.path.exists(log_path):
        print("Transcript log not found!")
        exit(1)

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            # Find the step around 649 where write_to_file or replace_file_content was used on build_merged.py
            step_idx = data.get('step_index')
            tool_calls = data.get('tool_calls', [])
            for tc in tool_calls:
                if tc.get('name') == 'write_to_file' and 'build_merged.py' in tc.get('args', {}).get('TargetFile', ''):
                    print(f"Found write_to_file on build_merged.py at step {step_idx}")
                    # Save this content to a temporary file
                    content = tc.get('args', {}).get('CodeContent', '')
                    if content:
                        with open(f"step_{step_idx}_build_merged.py", "w", encoding="utf-8") as out:
                            out.write(content)
                        print(f"Saved step_{step_idx}_build_merged.py")
        except Exception as e:
            pass
