export const brandsUrl = (
  domain: string,
  type: "icon" | "logo",
  useFallback?: boolean
): string =>
  `https://tech.automacaoraceland.pt/brands/${
    useFallback ? "_/" : ""
  }${domain}/${type}.png`;
