import re

# Open the .srt file
with open('source_files/DJI_0076.srt', 'r') as file:
    srt_text = file.read()

# Extract the times
times = re.findall(r'(\d{2}:\d{2}:\d{2},\d{3})', srt_text)

# Convert to milliseconds
times_in_milliseconds = []
for time in times:
    h, m, s_ms = time.split(':')
    s, ms = s_ms.split(',')
    total_ms = int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)
    times_in_milliseconds.append(total_ms)

print([times_in_milliseconds[i] for i in range(100,200)])
