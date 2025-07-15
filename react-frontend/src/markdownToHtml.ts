// src/markdownToHtml.ts

/**
 * Convierte texto tipo Markdown o wiki a HTML robusto y uniforme para respuestas de IA.
 * - Saltos de línea dobles: <p>...</p>
 * - Líneas que terminan en ':' (títulos): <strong>...</strong>
 * - Listas: <ul><li>...</li></ul>
 * - Negritas y cursivas
 */
export function markdownToHtml(markdown: string): string {
  if (!markdown) return '';
  let text = markdown.trim();

  // Negritas: **texto** o __texto__
  text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/__(.*?)__/g, '<strong>$1</strong>');

  // Cursivas: *texto* o _texto_
  text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
  text = text.replace(/_(.*?)_/g, '<em>$1</em>');

  // Procesar listas agrupadas
  // Detectar bloques de líneas que empiezan con - o *
  text = text.replace(/((?:^|\n)[\*-] .*(?:\n[\*-] .*)*)/gm, (match) => {
    // Quitar saltos de línea iniciales
    const items = match.trim().split(/\n/).map(line => line.replace(/^[\*-] /, '').trim());
    return `<ul>${items.map(i => `<li>${i}</li>`).join('')}</ul>`;
  });

  // Títulos: línea sola que termina en : (no dentro de lista)
  text = text.replace(/(^|\n)([^\n<]+:)(?=\n|$)/g, (m, pre, title) => {
    // Si ya está dentro de <li> o <ul>, no lo toques
    if (pre.includes('</li>') || pre.includes('</ul>')) return m;
    return `${pre}<strong>${title}</strong>`;
  });

  // Saltos de línea dobles a párrafos
  text = text.replace(/\n{2,}/g, '</p><p>');
  // Envolver todo en <p> si no está dentro de lista
  text = `<p>${text}</p>`;
  // Quitar <p> dentro de <ul> o <li>
  text = text.replace(/<ul><p>/g, '<ul>');
  text = text.replace(/<\/p><\/ul>/g, '</ul>');
  text = text.replace(/<li><p>/g, '<li>');
  text = text.replace(/<\/p><\/li>/g, '</li>');

  // Saltos de línea simples a <br> (solo fuera de listas y párrafos)
  text = text.replace(/(?<!<\/p>)(?<!<\/li>)\n/g, '<br/>');

  return text;
} 