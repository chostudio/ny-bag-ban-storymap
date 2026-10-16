# Bagged by the Rules

StoryMap for Activity 1.3 (Institutions and Human Behavior): how formal and informal institutions shape bag use under New York State's plastic bag ban.

`index.html` is generated: edit `src.html`, then run

```
python3 -c "s=open('src.html').read(); open('index.html','w').write(s.replace('<!--CONCEPT-->', open('concept.svg.part').read()))"
```

`concept.svg.part` comes from `python3 build_concept.py plastic-bag-ban-concept-map.excalidraw`.
