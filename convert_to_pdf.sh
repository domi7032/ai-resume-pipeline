#!/bin/bash
soffice --headless --convert-to pdf ~/job-search/applications/*.docx --outdir ~/job-search/applications/
echo "转换完成！"
