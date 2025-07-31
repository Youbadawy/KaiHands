enum TabOption {
  PLANNER = "planner",
  BROWSER = "browser",
  JUPYTER = "jupyter",
  VSCODE = "vscode",
  SOCIAL_MEDIA = "social-media",
}

type TabType =
  | TabOption.PLANNER
  | TabOption.BROWSER
  | TabOption.JUPYTER
  | TabOption.VSCODE
  | TabOption.SOCIAL_MEDIA;

const AllTabs = [
  TabOption.VSCODE,
  TabOption.BROWSER,
  TabOption.PLANNER,
  TabOption.JUPYTER,
  TabOption.SOCIAL_MEDIA,
];

export { AllTabs, TabOption, type TabType };
