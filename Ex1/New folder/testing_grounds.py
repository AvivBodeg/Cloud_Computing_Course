import re
text = "sa-ds,  dsa!@#"
text = re.sub(r"[^\w\s-]", " ", text)
print(text.split())
if not text:
    print(1)

# lifespan_text = "up to years"
# nums = re.findall(r"(\d+)", str(lifespan_text))
# print(nums)

# print(min(nums) if nums else None)