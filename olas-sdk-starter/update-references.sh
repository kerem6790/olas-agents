#!/bin/bash

# Tüm dosyalarda keremgegek -> keremgegek ve agent-smith -> agent-smith değişikliklerini yap
find . -type f -not -path "*/\.*" -exec sed -i '' 's/keremgegek/keremgegek/g' {} +
find . -type f -not -path "*/\.*" -exec sed -i '' 's/agent-smith/agent-smith/g' {} +

echo "✅ Referanslar güncellendi!" 