You are given a task to integrate an existing React component in the codebase

The codebase should support:
- shadcn project structure  
- Tailwind CSS
- Typescript

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind or Typescript.

Determine the default path for components and styles. 
If default path for components is not /components/ui, provide instructions on why it's important to create this folder
Copy-paste this component to /components/ui folder:
```tsx
display-cards.tsx
"use client";

import { cn } from "@/lib/utils";
import { Sparkles } from "lucide-react";

interface DisplayCardProps {
  className?: string;
  icon?: React.ReactNode;
  title?: string;
  description?: string;
  date?: string;
  iconClassName?: string;
  titleClassName?: string;
}

function DisplayCard({
  className,
  icon = <Sparkles className="size-4 text-blue-300" />,
  title = "Featured",
  description = "Discover amazing content",
  date = "Just now",
  iconClassName = "text-blue-500",
  titleClassName = "text-blue-500",
}: DisplayCardProps) {
  return (
    <div
      className={cn(
        "relative flex h-36 w-[22rem] -skew-y-[8deg] select-none flex-col justify-between rounded-xl border-2 bg-muted/70 backdrop-blur-sm px-4 py-3 transition-all duration-700 after:absolute after:-right-1 after:top-[-5%] after:h-[110%] after:w-[20rem] after:bg-gradient-to-l after:from-background after:to-transparent after:content-[''] hover:border-white/20 hover:bg-muted [&>*]:flex [&>*]:items-center [&>*]:gap-2",
        className
      )}
    >
      <div>
        <span className="relative inline-block rounded-full bg-blue-800 p-1">
          {icon}
        </span>
        <p className={cn("text-lg font-medium", titleClassName)}>{title}</p>
      </div>
      <p className="whitespace-nowrap text-lg">{description}</p>
      <p className="text-muted-foreground">{date}</p>
    </div>
  );
}

interface DisplayCardsProps {
  cards?: DisplayCardProps[];
}

export default function DisplayCards({ cards }: DisplayCardsProps) {
  const defaultCards = [
    {
      className: "[grid-area:stack] hover:-translate-y-10 before:absolute before:w-[100%] before:outline-1 before:rounded-xl before:outline-border before:h-[100%] before:content-[''] before:bg-blend-overlay before:bg-background/50 grayscale-[100%] hover:before:opacity-0 before:transition-opacity before:duration:700 hover:grayscale-0 before:left-0 before:top-0",
    },
    {
      className: "[grid-area:stack] translate-x-16 translate-y-10 hover:-translate-y-1 before:absolute before:w-[100%] before:outline-1 before:rounded-xl before:outline-border before:h-[100%] before:content-[''] before:bg-blend-overlay before:bg-background/50 grayscale-[100%] hover:before:opacity-0 before:transition-opacity before:duration:700 hover:grayscale-0 before:left-0 before:top-0",
    },
    {
      className: "[grid-area:stack] translate-x-32 translate-y-20 hover:translate-y-10",
    },
  ];

  const displayCards = cards || defaultCards;

  return (
    <div className="grid [grid-template-areas:'stack'] place-items-center opacity-100 animate-in fade-in-0 duration-700">
      {displayCards.map((cardProps, index) => (
        <DisplayCard key={index} {...cardProps} />
      ))}
    </div>
  );
}

demo.tsx
"use client";

import DisplayCards from "@/components/ui/display-cards";
import { Sparkles } from "lucide-react";

const defaultCards = [
  {
    icon: <Sparkles className="size-4 text-blue-300" />,
    title: "Featured",
    description: "Discover amazing content",
    date: "Just now",
    iconClassName: "text-blue-500",
    titleClassName: "text-blue-500",
    className:
      "[grid-area:stack] hover:-translate-y-10 before:absolute before:w-[100%] before:outline-1 before:rounded-xl before:outline-border before:h-[100%] before:content-[''] before:bg-blend-overlay before:bg-background/50 grayscale-[100%] hover:before:opacity-0 before:transition-opacity before:duration-700 hover:grayscale-0 before:left-0 before:top-0",
  },
  {
    icon: <Sparkles className="size-4 text-blue-300" />,
    title: "Popular",
    description: "Trending this week",
    date: "2 days ago",
    iconClassName: "text-blue-500",
    titleClassName: "text-blue-500",
    className:
      "[grid-area:stack] translate-x-12 translate-y-10 hover:-translate-y-1 before:absolute before:w-[100%] before:outline-1 before:rounded-xl before:outline-border before:h-[100%] before:content-[''] before:bg-blend-overlay before:bg-background/50 grayscale-[100%] hover:before:opacity-0 before:transition-opacity before:duration-700 hover:grayscale-0 before:left-0 before:top-0",
  },
  {
    icon: <Sparkles className="size-4 text-blue-300" />,
    title: "New",
    description: "Latest updates and features",
    date: "Today",
    iconClassName: "text-blue-500",
    titleClassName: "text-blue-500",
    className:
      "[grid-area:stack] translate-x-24 translate-y-20 hover:translate-y-10",
  },
];

function DisplayCardsDemo() {
  return (
    <div className="flex min-h-[400px] w-full items-center justify-center py-20">
      <div className="w-full max-w-3xl">
        <DisplayCards cards={defaultCards} />
      </div>
    </div>
  );
}

export { DisplayCardsDemo };

```

Install NPM dependencies:
```bash
lucide-react
```

Implementation Guidelines
 1. Analyze the component structure and identify all required dependencies
 2. Review the component's argumens and state
 3. Identify any required context providers or hooks and install them
 4. Questions to Ask
 - What data/props will be passed to this component?
 - Are there any specific state management requirements?
 - Are there any required assets (images, icons, etc.)?
 - What is the expected responsive behavior?
 - What is the best place to use this component in the app?

Steps to integrate
 0. Copy paste all the code above in the correct directories
 1. Install external dependencies
 2. Fill image assets with Unsplash stock images you know exist
 3. Use lucide-react icons for svgs or logos if component requires them


:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

You are given a task to integrate an existing React component in the codebase

The codebase should support:
- shadcn project structure  
- Tailwind CSS
- Typescript

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind or Typescript.

Determine the default path for components and styles. 
If default path for components is not /components/ui, provide instructions on why it's important to create this folder
Copy-paste this component to /components/ui folder:
```tsx
display-cards.tsx
"use client";

import { cn } from "@/lib/utils";
import { Sparkles } from "lucide-react";

interface DisplayCardProps {
  className?: string;
  icon?: React.ReactNode;
  title?: string;
  description?: string;
  date?: string;
  iconClassName?: string;
  titleClassName?: string;
}

function DisplayCard({
  className,
  icon = <Sparkles className="size-4 text-blue-300" />,
  title = "Featured",
  description = "Discover amazing content",
  date = "Just now",
  iconClassName = "text-blue-500",
  titleClassName = "text-blue-500",
}: DisplayCardProps) {
  return (
    <div
      className={cn(
        "relative flex h-36 w-[22rem] -skew-y-[8deg] select-none flex-col justify-between rounded-xl border-2 bg-muted/70 backdrop-blur-sm px-4 py-3 transition-all duration-700 after:absolute after:-right-1 after:top-[-5%] after:h-[110%] after:w-[20rem] after:bg-gradient-to-l after:from-background after:to-transparent after:content-[''] hover:border-white/20 hover:bg-muted [&>*]:flex [&>*]:items-center [&>*]:gap-2",
        className
      )}
    >
      <div>
        <span className="relative inline-block rounded-full bg-blue-800 p-1">
          {icon}
        </span>
        <p className={cn("text-lg font-medium", titleClassName)}>{title}</p>
      </div>
      <p className="whitespace-nowrap text-lg">{description}</p>
      <p className="text-muted-foreground">{date}</p>
    </div>
  );
}

interface DisplayCardsProps {
  cards?: DisplayCardProps[];
}

export default function DisplayCards({ cards }: DisplayCardsProps) {
  const defaultCards = [
    {
      className: "[grid-area:stack] hover:-translate-y-10 before:absolute before:w-[100%] before:outline-1 before:rounded-xl before:outline-border before:h-[100%] before:content-[''] before:bg-blend-overlay before:bg-background/50 grayscale-[100%] hover:before:opacity-0 before:transition-opacity before:duration:700 hover:grayscale-0 before:left-0 before:top-0",
    },
    {
      className: "[grid-area:stack] translate-x-16 translate-y-10 hover:-translate-y-1 before:absolute before:w-[100%] before:outline-1 before:rounded-xl before:outline-border before:h-[100%] before:content-[''] before:bg-blend-overlay before:bg-background/50 grayscale-[100%] hover:before:opacity-0 before:transition-opacity before:duration:700 hover:grayscale-0 before:left-0 before:top-0",
    },
    {
      className: "[grid-area:stack] translate-x-32 translate-y-20 hover:translate-y-10",
    },
  ];

  const displayCards = cards || defaultCards;

  return (
    <div className="grid [grid-template-areas:'stack'] place-items-center opacity-100 animate-in fade-in-0 duration-700">
      {displayCards.map((cardProps, index) => (
        <DisplayCard key={index} {...cardProps} />
      ))}
    </div>
  );
}

demo.tsx
"use client";

import DisplayCards from "@/components/ui/display-cards";
import { Sparkles } from "lucide-react";

const defaultCards = [
  {
    icon: <Sparkles className="size-4 text-blue-300" />,
    title: "Featured",
    description: "Discover amazing content",
    date: "Just now",
    iconClassName: "text-blue-500",
    titleClassName: "text-blue-500",
    className:
      "[grid-area:stack] hover:-translate-y-10 before:absolute before:w-[100%] before:outline-1 before:rounded-xl before:outline-border before:h-[100%] before:content-[''] before:bg-blend-overlay before:bg-background/50 grayscale-[100%] hover:before:opacity-0 before:transition-opacity before:duration-700 hover:grayscale-0 before:left-0 before:top-0",
  },
  {
    icon: <Sparkles className="size-4 text-blue-300" />,
    title: "Popular",
    description: "Trending this week",
    date: "2 days ago",
    iconClassName: "text-blue-500",
    titleClassName: "text-blue-500",
    className:
      "[grid-area:stack] translate-x-12 translate-y-10 hover:-translate-y-1 before:absolute before:w-[100%] before:outline-1 before:rounded-xl before:outline-border before:h-[100%] before:content-[''] before:bg-blend-overlay before:bg-background/50 grayscale-[100%] hover:before:opacity-0 before:transition-opacity before:duration-700 hover:grayscale-0 before:left-0 before:top-0",
  },
  {
    icon: <Sparkles className="size-4 text-blue-300" />,
    title: "New",
    description: "Latest updates and features",
    date: "Today",
    iconClassName: "text-blue-500",
    titleClassName: "text-blue-500",
    className:
      "[grid-area:stack] translate-x-24 translate-y-20 hover:translate-y-10",
  },
];

function DisplayCardsDemo() {
  return (
    <div className="flex min-h-[400px] w-full items-center justify-center py-20">
      <div className="w-full max-w-3xl">
        <DisplayCards cards={defaultCards} />
      </div>
    </div>
  );
}

export { DisplayCardsDemo };

```

Install NPM dependencies:
```bash
lucide-react
```

Implementation Guidelines
 1. Analyze the component structure and identify all required dependencies
 2. Review the component's argumens and state
 3. Identify any required context providers or hooks and install them
 4. Questions to Ask
 - What data/props will be passed to this component?
 - Are there any specific state management requirements?
 - Are there any required assets (images, icons, etc.)?
 - What is the expected responsive behavior?
 - What is the best place to use this component in the app?

Steps to integrate
 0. Copy paste all the code above in the correct directories
 1. Install external dependencies
 2. Fill image assets with Unsplash stock images you know exist
 3. Use lucide-react icons for svgs or logos if component requires them

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

You are given a task to integrate an existing React component in the codebase

The codebase should support:
- shadcn project structure  
- Tailwind CSS
- Typescript

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind or Typescript.

Determine the default path for components and styles. 
If default path for components is not /components/ui, provide instructions on why it's important to create this folder
Copy-paste this component to /components/ui folder:
```tsx
radial-orbital-timeline.tsx
"use client";
import { useState, useEffect, useRef } from "react";
import { ArrowRight, Link, Zap } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface TimelineItem {
  id: number;
  title: string;
  date: string;
  content: string;
  category: string;
  icon: React.ElementType;
  relatedIds: number[];
  status: "completed" | "in-progress" | "pending";
  energy: number;
}

interface RadialOrbitalTimelineProps {
  timelineData: TimelineItem[];
}

export default function RadialOrbitalTimeline({
  timelineData,
}: RadialOrbitalTimelineProps) {
  const [expandedItems, setExpandedItems] = useState<Record<number, boolean>>(
    {}
  );
  const [viewMode, setViewMode] = useState<"orbital">("orbital");
  const [rotationAngle, setRotationAngle] = useState<number>(0);
  const [autoRotate, setAutoRotate] = useState<boolean>(true);
  const [pulseEffect, setPulseEffect] = useState<Record<number, boolean>>({});
  const [centerOffset, setCenterOffset] = useState<{ x: number; y: number }>({
    x: 0,
    y: 0,
  });
  const [activeNodeId, setActiveNodeId] = useState<number | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const orbitRef = useRef<HTMLDivElement>(null);
  const nodeRefs = useRef<Record<number, HTMLDivElement | null>>({});

  const handleContainerClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === containerRef.current || e.target === orbitRef.current) {
      setExpandedItems({});
      setActiveNodeId(null);
      setPulseEffect({});
      setAutoRotate(true);
    }
  };

  const toggleItem = (id: number) => {
    setExpandedItems((prev) => {
      const newState = { ...prev };
      Object.keys(newState).forEach((key) => {
        if (parseInt(key) !== id) {
          newState[parseInt(key)] = false;
        }
      });

      newState[id] = !prev[id];

      if (!prev[id]) {
        setActiveNodeId(id);
        setAutoRotate(false);

        const relatedItems = getRelatedItems(id);
        const newPulseEffect: Record<number, boolean> = {};
        relatedItems.forEach((relId) => {
          newPulseEffect[relId] = true;
        });
        setPulseEffect(newPulseEffect);

        centerViewOnNode(id);
      } else {
        setActiveNodeId(null);
        setAutoRotate(true);
        setPulseEffect({});
      }

      return newState;
    });
  };

  useEffect(() => {
    let rotationTimer: NodeJS.Timeout;

    if (autoRotate && viewMode === "orbital") {
      rotationTimer = setInterval(() => {
        setRotationAngle((prev) => {
          const newAngle = (prev + 0.3) % 360;
          return Number(newAngle.toFixed(3));
        });
      }, 50);
    }

    return () => {
      if (rotationTimer) {
        clearInterval(rotationTimer);
      }
    };
  }, [autoRotate, viewMode]);

  const centerViewOnNode = (nodeId: number) => {
    if (viewMode !== "orbital" || !nodeRefs.current[nodeId]) return;

    const nodeIndex = timelineData.findIndex((item) => item.id === nodeId);
    const totalNodes = timelineData.length;
    const targetAngle = (nodeIndex / totalNodes) * 360;

    setRotationAngle(270 - targetAngle);
  };

  const calculateNodePosition = (index: number, total: number) => {
    const angle = ((index / total) * 360 + rotationAngle) % 360;
    const radius = 200;
    const radian = (angle * Math.PI) / 180;

    const x = radius * Math.cos(radian) + centerOffset.x;
    const y = radius * Math.sin(radian) + centerOffset.y;

    const zIndex = Math.round(100 + 50 * Math.cos(radian));
    const opacity = Math.max(
      0.4,
      Math.min(1, 0.4 + 0.6 * ((1 + Math.sin(radian)) / 2))
    );

    return { x, y, angle, zIndex, opacity };
  };

  const getRelatedItems = (itemId: number): number[] => {
    const currentItem = timelineData.find((item) => item.id === itemId);
    return currentItem ? currentItem.relatedIds : [];
  };

  const isRelatedToActive = (itemId: number): boolean => {
    if (!activeNodeId) return false;
    const relatedItems = getRelatedItems(activeNodeId);
    return relatedItems.includes(itemId);
  };

  const getStatusStyles = (status: TimelineItem["status"]): string => {
    switch (status) {
      case "completed":
        return "text-white bg-black border-white";
      case "in-progress":
        return "text-black bg-white border-black";
      case "pending":
        return "text-white bg-black/40 border-white/50";
      default:
        return "text-white bg-black/40 border-white/50";
    }
  };

  return (
    <div
      className="w-full h-screen flex flex-col items-center justify-center bg-black overflow-hidden"
      ref={containerRef}
      onClick={handleContainerClick}
    >
      <div className="relative w-full max-w-4xl h-full flex items-center justify-center">
        <div
          className="absolute w-full h-full flex items-center justify-center"
          ref={orbitRef}
          style={{
            perspective: "1000px",
            transform: `translate(${centerOffset.x}px, ${centerOffset.y}px)`,
          }}
        >
          <div className="absolute w-16 h-16 rounded-full bg-gradient-to-br from-purple-500 via-blue-500 to-teal-500 animate-pulse flex items-center justify-center z-10">
            <div className="absolute w-20 h-20 rounded-full border border-white/20 animate-ping opacity-70"></div>
            <div
              className="absolute w-24 h-24 rounded-full border border-white/10 animate-ping opacity-50"
              style={{ animationDelay: "0.5s" }}
            ></div>
            <div className="w-8 h-8 rounded-full bg-white/80 backdrop-blur-md"></div>
          </div>

          <div className="absolute w-96 h-96 rounded-full border border-white/10"></div>

          {timelineData.map((item, index) => {
            const position = calculateNodePosition(index, timelineData.length);
            const isExpanded = expandedItems[item.id];
            const isRelated = isRelatedToActive(item.id);
            const isPulsing = pulseEffect[item.id];
            const Icon = item.icon;

            const nodeStyle = {
              transform: `translate(${position.x}px, ${position.y}px)`,
              zIndex: isExpanded ? 200 : position.zIndex,
              opacity: isExpanded ? 1 : position.opacity,
            };

            return (
              <div
                key={item.id}
                ref={(el) => (nodeRefs.current[item.id] = el)}
                className="absolute transition-all duration-700 cursor-pointer"
                style={nodeStyle}
                onClick={(e) => {
                  e.stopPropagation();
                  toggleItem(item.id);
                }}
              >
                <div
                  className={`absolute rounded-full -inset-1 ${
                    isPulsing ? "animate-pulse duration-1000" : ""
                  }`}
                  style={{
                    background: `radial-gradient(circle, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 70%)`,
                    width: `${item.energy * 0.5 + 40}px`,
                    height: `${item.energy * 0.5 + 40}px`,
                    left: `-${(item.energy * 0.5 + 40 - 40) / 2}px`,
                    top: `-${(item.energy * 0.5 + 40 - 40) / 2}px`,
                  }}
                ></div>

                <div
                  className={`
                  w-10 h-10 rounded-full flex items-center justify-center
                  ${
                    isExpanded
                      ? "bg-white text-black"
                      : isRelated
                      ? "bg-white/50 text-black"
                      : "bg-black text-white"
                  }
                  border-2 
                  ${
                    isExpanded
                      ? "border-white shadow-lg shadow-white/30"
                      : isRelated
                      ? "border-white animate-pulse"
                      : "border-white/40"
                  }
                  transition-all duration-300 transform
                  ${isExpanded ? "scale-150" : ""}
                `}
                >
                  <Icon size={16} />
                </div>

                <div
                  className={`
                  absolute top-12  whitespace-nowrap
                  text-xs font-semibold tracking-wider
                  transition-all duration-300
                  ${isExpanded ? "text-white scale-125" : "text-white/70"}
                `}
                >
                  {item.title}
                </div>

                {isExpanded && (
                  <Card className="absolute top-20 left-1/2 -translate-x-1/2 w-64 bg-black/90 backdrop-blur-lg border-white/30 shadow-xl shadow-white/10 overflow-visible">
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 w-px h-3 bg-white/50"></div>
                    <CardHeader className="pb-2">
                      <div className="flex justify-between items-center">
                        <Badge
                          className={`px-2 text-xs ${getStatusStyles(
                            item.status
                          )}`}
                        >
                          {item.status === "completed"
                            ? "COMPLETE"
                            : item.status === "in-progress"
                            ? "IN PROGRESS"
                            : "PENDING"}
                        </Badge>
                        <span className="text-xs font-mono text-white/50">
                          {item.date}
                        </span>
                      </div>
                      <CardTitle className="text-sm mt-2">
                        {item.title}
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="text-xs text-white/80">
                      <p>{item.content}</p>

                      <div className="mt-4 pt-3 border-t border-white/10">
                        <div className="flex justify-between items-center text-xs mb-1">
                          <span className="flex items-center">
                            <Zap size={10} className="mr-1" />
                            Energy Level
                          </span>
                          <span className="font-mono">{item.energy}%</span>
                        </div>
                        <div className="w-full h-1 bg-white/10 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-blue-500 to-purple-500"
                            style={{ width: `${item.energy}%` }}
                          ></div>
                        </div>
                      </div>

                      {item.relatedIds.length > 0 && (
                        <div className="mt-4 pt-3 border-t border-white/10">
                          <div className="flex items-center mb-2">
                            <Link size={10} className="text-white/70 mr-1" />
                            <h4 className="text-xs uppercase tracking-wider font-medium text-white/70">
                              Connected Nodes
                            </h4>
                          </div>
                          <div className="flex flex-wrap gap-1">
                            {item.relatedIds.map((relatedId) => {
                              const relatedItem = timelineData.find(
                                (i) => i.id === relatedId
                              );
                              return (
                                <Button
                                  key={relatedId}
                                  variant="outline"
                                  size="sm"
                                  className="flex items-center h-6 px-2 py-0 text-xs rounded-none border-white/20 bg-transparent hover:bg-white/10 text-white/80 hover:text-white transition-all"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    toggleItem(relatedId);
                                  }}
                                >
                                  {relatedItem?.title}
                                  <ArrowRight
                                    size={8}
                                    className="ml-1 text-white/60"
                                  />
                                </Button>
                              );
                            })}
                          </div>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}


demo.tsx
"use client";

import { Calendar, Code, FileText, User, Clock } from "lucide-react";
import RadialOrbitalTimeline from "@/components/ui/radial-orbital-timeline";

const timelineData = [
  {
    id: 1,
    title: "Planning",
    date: "Jan 2024",
    content: "Project planning and requirements gathering phase.",
    category: "Planning",
    icon: Calendar,
    relatedIds: [2],
    status: "completed" as const,
    energy: 100,
  },
  {
    id: 2,
    title: "Design",
    date: "Feb 2024",
    content: "UI/UX design and system architecture.",
    category: "Design",
    icon: FileText,
    relatedIds: [1, 3],
    status: "completed" as const,
    energy: 90,
  },
  {
    id: 3,
    title: "Development",
    date: "Mar 2024",
    content: "Core features implementation and testing.",
    category: "Development",
    icon: Code,
    relatedIds: [2, 4],
    status: "in-progress" as const,
    energy: 60,
  },
  {
    id: 4,
    title: "Testing",
    date: "Apr 2024",
    content: "User testing and bug fixes.",
    category: "Testing",
    icon: User,
    relatedIds: [3, 5],
    status: "pending" as const,
    energy: 30,
  },
  {
    id: 5,
    title: "Release",
    date: "May 2024",
    content: "Final deployment and release.",
    category: "Release",
    icon: Clock,
    relatedIds: [4],
    status: "pending" as const,
    energy: 10,
  },
];

export function RadialOrbitalTimelineDemo() {
  return (
    <>
      <RadialOrbitalTimeline timelineData={timelineData} />
    </>
  );
}

export default {
  RadialOrbitalTimelineDemo,
};

```

Copy-paste these files for dependencies:
```tsx
shadcn/badge
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default:
          "border-transparent bg-primary text-primary-foreground hover:bg-primary/80",
        secondary:
          "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
        destructive:
          "border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80",
        outline: "text-foreground",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  },
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }

```
```tsx
shadcn/button
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive:
          "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline:
          "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary:
          "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  },
)
Button.displayName = "Button"

export { Button, buttonVariants }

```
```tsx
shadcn/card
import * as React from "react"

import { cn } from "@/lib/utils"

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-lg border bg-card text-card-foreground shadow-sm",
      className,
    )}
    {...props}
  />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props}
  />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "text-2xl font-semibold leading-none tracking-tight",
      className,
    )}
    {...props}
  />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0", className)}
    {...props}
  />
))
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }

```

Install NPM dependencies:
```bash
lucide-react, class-variance-authority, @radix-ui/react-slot
```

Extend existing globals.css with this code:
```css
@import "tailwindcss"

/* Animation for the pulsing effect */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Animation for the ping effect */
@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

/* Custom animations for the orbital timeline */
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-ping {
  animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite;
}

/* Transitions */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

.duration-300 {
  transition-duration: 300ms;
}

.duration-700 {
  transition-duration: 700ms;
}

.duration-1000 {
  transition-duration: 1000ms;
}

/* Backdrop blur */
.backdrop-blur-lg {
  backdrop-filter: blur(16px);
}

/* Custom gradients */
.bg-gradient-orbital {
  background: linear-gradient(to bottom right, #6366f1, #3b82f6, #14b8a6);
}

/* Z-index utilities */
.z-10 {
  z-index: 10;
}

.z-50 {
  z-index: 50;
}

/* Custom shadows */
.shadow-orbital {
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
}

/* Custom transforms */
.scale-125 {
  transform: scale(1.25);
}

.scale-150 {
  transform: scale(1.5);
}

/* Custom opacity values */
.opacity-70 {
  opacity: 0.7;
}

.opacity-50 {
  opacity: 0.5;
}

/* Custom border opacity */
.border-white\/10 {
  border-color: rgba(255, 255, 255, 0.1);
}

.border-white\/20 {
  border-color: rgba(255, 255, 255, 0.2);
}

.border-white\/30 {
  border-color: rgba(255, 255, 255, 0.3);
}

.border-white\/40 {
  border-color: rgba(255, 255, 255, 0.4);
}

/* Custom background opacity */
.bg-black\/90 {
  background-color: rgba(0, 0, 0, 0.9);
}

.bg-white\/50 {
  background-color: rgba(255, 255, 255, 0.5);
}

.bg-white\/80 {
  background-color: rgba(255, 255, 255, 0.8);
}

/* Custom text opacity */
.text-white\/70 {
  color: rgba(255, 255, 255, 0.7);
}

.text-white\/80 {
  color: rgba(255, 255, 255, 0.8);
} 
```

Implementation Guidelines
 1. Analyze the component structure and identify all required dependencies
 2. Review the component's argumens and state
 3. Identify any required context providers or hooks and install them
 4. Questions to Ask
 - What data/props will be passed to this component?
 - Are there any specific state management requirements?
 - Are there any required assets (images, icons, etc.)?
 - What is the expected responsive behavior?
 - What is the best place to use this component in the app?

Steps to integrate
 0. Copy paste all the code above in the correct directories
 1. Install external dependencies
 2. Fill image assets with Unsplash stock images you know exist
 3. Use lucide-react icons for svgs or logos if component requires them


::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

You are given a task to integrate an existing React component in the codebase

The codebase should support:
- shadcn project structure  
- Tailwind CSS
- Typescript

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind or Typescript.

Determine the default path for components and styles. 
If default path for components is not /components/ui, provide instructions on why it's important to create this folder
Copy-paste this component to /components/ui folder:
```tsx
sign-in-flow-1.tsx
"use client";

import React, { useState,useMemo, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import { cn } from "@/lib/utils";
import { Canvas, useFrame, useThree } from "@react-three/fiber";

import * as THREE from "three";

type Uniforms = {
  [key: string]: {
    value: number[] | number[][] | number;
    type: string;
  };
};

interface ShaderProps {
  source: string;
  uniforms: {
    [key: string]: {
      value: number[] | number[][] | number;
      type: string;
    };
  };
  maxFps?: number;
}

interface SignInPageProps {
  className?: string;
}
      
export const CanvasRevealEffect = ({
  animationSpeed = 10,
  opacities = [0.3, 0.3, 0.3, 0.5, 0.5, 0.5, 0.8, 0.8, 0.8, 1],
  colors = [[0, 255, 255]],
  containerClassName,
  dotSize,
  showGradient = true,
  reverse = false, // This controls the direction
}: {
  animationSpeed?: number;
  opacities?: number[];
  colors?: number[][];
  containerClassName?: string;
  dotSize?: number;
  showGradient?: boolean;
  reverse?: boolean; // This prop determines the direction
}) => {
  return (
    <div className={cn("h-full relative w-full", containerClassName)}> {/* Removed bg-white */}
      <div className="h-full w-full">
        <DotMatrix
          colors={colors ?? [[0, 255, 255]]}
          dotSize={dotSize ?? 3}
          opacities={
            opacities ?? [0.3, 0.3, 0.3, 0.5, 0.5, 0.5, 0.8, 0.8, 0.8, 1]
          }
          // Pass reverse state and speed via string flags in the empty shader prop
          shader={`
            ${reverse ? 'u_reverse_active' : 'false'}_;
            animation_speed_factor_${animationSpeed.toFixed(1)}_;
          `}
          center={["x", "y"]}
        />
      </div>
      {showGradient && (
        // Adjust gradient colors if needed based on background (was bg-white, now likely uses containerClassName bg)
        // Example assuming a dark background like the SignInPage uses:
         <div className="absolute inset-0 bg-gradient-to-t from-black to-transparent" />
      )}
    </div>
  );
};

    
interface DotMatrixProps {
  colors?: number[][];
  opacities?: number[];
  totalSize?: number;
  dotSize?: number;
  shader?: string;
  center?: ("x" | "y")[];
}

const DotMatrix: React.FC<DotMatrixProps> = ({
  colors = [[0, 0, 0]],
  opacities = [0.04, 0.04, 0.04, 0.04, 0.04, 0.08, 0.08, 0.08, 0.08, 0.14],
  totalSize = 20,
  dotSize = 2,
  shader = "", // This shader string will now contain the animation logic
  center = ["x", "y"],
}) => {
  // ... uniforms calculation remains the same for colors, opacities, etc.
  const uniforms = React.useMemo(() => {
    let colorsArray = [
      colors[0],
      colors[0],
      colors[0],
      colors[0],
      colors[0],
      colors[0],
    ];
    if (colors.length === 2) {
      colorsArray = [
        colors[0],
        colors[0],
        colors[0],
        colors[1],
        colors[1],
        colors[1],
      ];
    } else if (colors.length === 3) {
      colorsArray = [
        colors[0],
        colors[0],
        colors[1],
        colors[1],
        colors[2],
        colors[2],
      ];
    }
    return {
      u_colors: {
        value: colorsArray.map((color) => [
          color[0] / 255,
          color[1] / 255,
          color[2] / 255,
        ]),
        type: "uniform3fv",
      },
      u_opacities: {
        value: opacities,
        type: "uniform1fv",
      },
      u_total_size: {
        value: totalSize,
        type: "uniform1f",
      },
      u_dot_size: {
        value: dotSize,
        type: "uniform1f",
      },
      u_reverse: {
        value: shader.includes("u_reverse_active") ? 1 : 0, // Convert boolean to number (1 or 0)
        type: "uniform1i", // Use 1i for bool in WebGL1/GLSL100, or just bool for GLSL300+ if supported
      },
    };
  }, [colors, opacities, totalSize, dotSize, shader]); // Add shader to dependencies

  return (
    <Shader
      // The main animation logic is now built *outside* the shader prop
      source={`
        precision mediump float;
        in vec2 fragCoord;

        uniform float u_time;
        uniform float u_opacities[10];
        uniform vec3 u_colors[6];
        uniform float u_total_size;
        uniform float u_dot_size;
        uniform vec2 u_resolution;
        uniform int u_reverse; // Changed from bool to int

        out vec4 fragColor;

        float PHI = 1.61803398874989484820459;
        float random(vec2 xy) {
            return fract(tan(distance(xy * PHI, xy) * 0.5) * xy.x);
        }
        float map(float value, float min1, float max1, float min2, float max2) {
            return min2 + (value - min1) * (max2 - min2) / (max1 - min1);
        }

        void main() {
            vec2 st = fragCoord.xy;
            ${
              center.includes("x")
                ? "st.x -= abs(floor((mod(u_resolution.x, u_total_size) - u_dot_size) * 0.5));"
                : ""
            }
            ${
              center.includes("y")
                ? "st.y -= abs(floor((mod(u_resolution.y, u_total_size) - u_dot_size) * 0.5));"
                : ""
            }

            float opacity = step(0.0, st.x);
            opacity *= step(0.0, st.y);

            vec2 st2 = vec2(int(st.x / u_total_size), int(st.y / u_total_size));

            float frequency = 5.0;
            float show_offset = random(st2); // Used for initial opacity random pick and color
            float rand = random(st2 * floor((u_time / frequency) + show_offset + frequency));
            opacity *= u_opacities[int(rand * 10.0)];
            opacity *= 1.0 - step(u_dot_size / u_total_size, fract(st.x / u_total_size));
            opacity *= 1.0 - step(u_dot_size / u_total_size, fract(st.y / u_total_size));

            vec3 color = u_colors[int(show_offset * 6.0)];

            // --- Animation Timing Logic ---
            float animation_speed_factor = 0.5; // Extract speed from shader string
            vec2 center_grid = u_resolution / 2.0 / u_total_size;
            float dist_from_center = distance(center_grid, st2);

            // Calculate timing offset for Intro (from center)
            float timing_offset_intro = dist_from_center * 0.01 + (random(st2) * 0.15);

            // Calculate timing offset for Outro (from edges)
            // Max distance from center to a corner of the grid
            float max_grid_dist = distance(center_grid, vec2(0.0, 0.0));
            float timing_offset_outro = (max_grid_dist - dist_from_center) * 0.02 + (random(st2 + 42.0) * 0.2);


            float current_timing_offset;
            if (u_reverse == 1) {
                current_timing_offset = timing_offset_outro;
                 // Outro logic: opacity starts high, goes to 0 when time passes offset
                 opacity *= 1.0 - step(current_timing_offset, u_time * animation_speed_factor);
                 // Clamp for fade-out transition
                 opacity *= clamp((step(current_timing_offset + 0.1, u_time * animation_speed_factor)) * 1.25, 1.0, 1.25);
            } else {
                current_timing_offset = timing_offset_intro;
                 // Intro logic: opacity starts 0, goes to base opacity when time passes offset
                 opacity *= step(current_timing_offset, u_time * animation_speed_factor);
                 // Clamp for fade-in transition
                 opacity *= clamp((1.0 - step(current_timing_offset + 0.1, u_time * animation_speed_factor)) * 1.25, 1.0, 1.25);
            }


            fragColor = vec4(color, opacity);
            fragColor.rgb *= fragColor.a; // Premultiply alpha
        }`}
      uniforms={uniforms}
      maxFps={60}
    />
  );
};


const ShaderMaterial = ({
  source,
  uniforms,
  maxFps = 60,
}: {
  source: string;
  hovered?: boolean;
  maxFps?: number;
  uniforms: Uniforms;
}) => {
  const { size } = useThree();
  const ref = useRef<THREE.Mesh>(null);
  let lastFrameTime = 0;

  useFrame(({ clock }) => {
    if (!ref.current) return;
    const timestamp = clock.getElapsedTime();

    lastFrameTime = timestamp;

    const material: any = ref.current.material;
    const timeLocation = material.uniforms.u_time;
    timeLocation.value = timestamp;
  });

  const getUniforms = () => {
    const preparedUniforms: any = {};

    for (const uniformName in uniforms) {
      const uniform: any = uniforms[uniformName];

      switch (uniform.type) {
        case "uniform1f":
          preparedUniforms[uniformName] = { value: uniform.value, type: "1f" };
          break;
        case "uniform1i":
          preparedUniforms[uniformName] = { value: uniform.value, type: "1i" };
          break;
        case "uniform3f":
          preparedUniforms[uniformName] = {
            value: new THREE.Vector3().fromArray(uniform.value),
            type: "3f",
          };
          break;
        case "uniform1fv":
          preparedUniforms[uniformName] = { value: uniform.value, type: "1fv" };
          break;
        case "uniform3fv":
          preparedUniforms[uniformName] = {
            value: uniform.value.map((v: number[]) =>
              new THREE.Vector3().fromArray(v)
            ),
            type: "3fv",
          };
          break;
        case "uniform2f":
          preparedUniforms[uniformName] = {
            value: new THREE.Vector2().fromArray(uniform.value),
            type: "2f",
          };
          break;
        default:
          console.error(`Invalid uniform type for '${uniformName}'.`);
          break;
      }
    }

    preparedUniforms["u_time"] = { value: 0, type: "1f" };
    preparedUniforms["u_resolution"] = {
      value: new THREE.Vector2(size.width * 2, size.height * 2),
    }; // Initialize u_resolution
    return preparedUniforms;
  };

  // Shader material
  const material = useMemo(() => {
    const materialObject = new THREE.ShaderMaterial({
      vertexShader: `
      precision mediump float;
      in vec2 coordinates;
      uniform vec2 u_resolution;
      out vec2 fragCoord;
      void main(){
        float x = position.x;
        float y = position.y;
        gl_Position = vec4(x, y, 0.0, 1.0);
        fragCoord = (position.xy + vec2(1.0)) * 0.5 * u_resolution;
        fragCoord.y = u_resolution.y - fragCoord.y;
      }
      `,
      fragmentShader: source,
      uniforms: getUniforms(),
      glslVersion: THREE.GLSL3,
      blending: THREE.CustomBlending,
      blendSrc: THREE.SrcAlphaFactor,
      blendDst: THREE.OneFactor,
    });

    return materialObject;
  }, [size.width, size.height, source]);

  return (
    <mesh ref={ref as any}>
      <planeGeometry args={[2, 2]} />
      <primitive object={material} attach="material" />
    </mesh>
  );
};

const Shader: React.FC<ShaderProps> = ({ source, uniforms, maxFps = 60 }) => {
  return (
    <Canvas className="absolute inset-0  h-full w-full">
      <ShaderMaterial source={source} uniforms={uniforms} maxFps={maxFps} />
    </Canvas>
  );
};

const AnimatedNavLink = ({ href, children }: { href: string; children: React.ReactNode }) => {
  const defaultTextColor = 'text-gray-300';
  const hoverTextColor = 'text-white';
  const textSizeClass = 'text-sm';

  return (
    <a href={href} className={`group relative inline-block overflow-hidden h-5 flex items-center ${textSizeClass}`}>
      <div className="flex flex-col transition-transform duration-400 ease-out transform group-hover:-translate-y-1/2">
        <span className={defaultTextColor}>{children}</span>
        <span className={hoverTextColor}>{children}</span>
      </div>
    </a>
  );
};

function MiniNavbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [headerShapeClass, setHeaderShapeClass] = useState('rounded-full');
  const shapeTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  useEffect(() => {
    if (shapeTimeoutRef.current) {
      clearTimeout(shapeTimeoutRef.current);
    }

    if (isOpen) {
      setHeaderShapeClass('rounded-xl');
    } else {
      shapeTimeoutRef.current = setTimeout(() => {
        setHeaderShapeClass('rounded-full');
      }, 300);
    }

    return () => {
      if (shapeTimeoutRef.current) {
        clearTimeout(shapeTimeoutRef.current);
      }
    };
  }, [isOpen]);

  const logoElement = (
    <div className="relative w-5 h-5 flex items-center justify-center">
    <span className="absolute w-1.5 h-1.5 rounded-full bg-gray-200 top-0 left-1/2 transform -translate-x-1/2 opacity-80"></span>
    <span className="absolute w-1.5 h-1.5 rounded-full bg-gray-200 left-0 top-1/2 transform -translate-y-1/2 opacity-80"></span>
    <span className="absolute w-1.5 h-1.5 rounded-full bg-gray-200 right-0 top-1/2 transform -translate-y-1/2 opacity-80"></span>
    <span className="absolute w-1.5 h-1.5 rounded-full bg-gray-200 bottom-0 left-1/2 transform -translate-x-1/2 opacity-80"></span>
 </div>
  );

  const navLinksData = [
    { label: 'Manifesto', href: '#1' },
    { label: 'Careers', href: '#2' },
    { label: 'Discover', href: '#3' },
  ];

  const loginButtonElement = (
    <button className="px-4 py-2 sm:px-3 text-xs sm:text-sm border border-[#333] bg-[rgba(31,31,31,0.62)] text-gray-300 rounded-full hover:border-white/50 hover:text-white transition-colors duration-200 w-full sm:w-auto">
      LogIn
    </button>
  );

  const signupButtonElement = (
    <div className="relative group w-full sm:w-auto">
       <div className="absolute inset-0 -m-2 rounded-full
                     hidden sm:block
                     bg-gray-100
                     opacity-40 filter blur-lg pointer-events-none
                     transition-all duration-300 ease-out
                     group-hover:opacity-60 group-hover:blur-xl group-hover:-m-3"></div>
       <button className="relative z-10 px-4 py-2 sm:px-3 text-xs sm:text-sm font-semibold text-black bg-gradient-to-br from-gray-100 to-gray-300 rounded-full hover:from-gray-200 hover:to-gray-400 transition-all duration-200 w-full sm:w-auto">
         Signup
       </button>
    </div>
  );

  return (
    <header className={`fixed top-6 left-1/2 transform -translate-x-1/2 z-20
                       flex flex-col items-center
                       pl-6 pr-6 py-3 backdrop-blur-sm
                       ${headerShapeClass}
                       border border-[#333] bg-[#1f1f1f57]
                       w-[calc(100%-2rem)] sm:w-auto
                       transition-[border-radius] duration-0 ease-in-out`}>

      <div className="flex items-center justify-between w-full gap-x-6 sm:gap-x-8">
        <div className="flex items-center">
           {logoElement}
        </div>

        <nav className="hidden sm:flex items-center space-x-4 sm:space-x-6 text-sm">
          {navLinksData.map((link) => (
            <AnimatedNavLink key={link.href} href={link.href}>
              {link.label}
            </AnimatedNavLink>
          ))}
        </nav>

        <div className="hidden sm:flex items-center gap-2 sm:gap-3">
          {loginButtonElement}
          {signupButtonElement}
        </div>

        <button className="sm:hidden flex items-center justify-center w-8 h-8 text-gray-300 focus:outline-none" onClick={toggleMenu} aria-label={isOpen ? 'Close Menu' : 'Open Menu'}>
          {isOpen ? (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          ) : (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
          )}
        </button>
      </div>

      <div className={`sm:hidden flex flex-col items-center w-full transition-all ease-in-out duration-300 overflow-hidden
                       ${isOpen ? 'max-h-[1000px] opacity-100 pt-4' : 'max-h-0 opacity-0 pt-0 pointer-events-none'}`}>
        <nav className="flex flex-col items-center space-y-4 text-base w-full">
          {navLinksData.map((link) => (
            <a key={link.href} href={link.href} className="text-gray-300 hover:text-white transition-colors w-full text-center">
              {link.label}
            </a>
          ))}
        </nav>
        <div className="flex flex-col items-center space-y-4 mt-4 w-full">
          {loginButtonElement}
          {signupButtonElement}
        </div>
      </div>
    </header>
  );
}

export const SignInPage = ({ className }: SignInPageProps) => {
  const [email, setEmail] = useState("");
  const [step, setStep] = useState<"email" | "code" | "success">("email");
  const [code, setCode] = useState(["", "", "", "", "", ""]);
  const codeInputRefs = useRef<(HTMLInputElement | null)[]>([]);
  const [showSuccessAnimation, setShowSuccessAnimation] = useState(false);
  const [initialCanvasVisible, setInitialCanvasVisible] = useState(true);
  const [reverseCanvasVisible, setReverseCanvasVisible] = useState(false);

  const handleEmailSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      setStep("code");
    }
  };

  // Focus first input when code screen appears
  useEffect(() => {
    if (step === "code") {
      setTimeout(() => {
        codeInputRefs.current[0]?.focus();
      }, 500);
    }
  }, [step]);

  const handleCodeChange = (index: number, value: string) => {
    if (value.length <= 1) {
      const newCode = [...code];
      newCode[index] = value;
      setCode(newCode);
      
      // Focus next input if value is entered
      if (value && index < 5) {
        codeInputRefs.current[index + 1]?.focus();
      }
      
      // Check if code is complete
      if (index === 5 && value) {
        const isComplete = newCode.every(digit => digit.length === 1);
        if (isComplete) {
          // First show the new reverse canvas
          setReverseCanvasVisible(true);
          
          // Then hide the original canvas after a small delay
          setTimeout(() => {
            setInitialCanvasVisible(false);
          }, 50);
          
          // Transition to success screen after animation
          setTimeout(() => {
            setStep("success");
          }, 2000);
        }
      }
    }
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Backspace" && !code[index] && index > 0) {
      codeInputRefs.current[index - 1]?.focus();
    }
  };

  const handleBackClick = () => {
    setStep("email");
    setCode(["", "", "", "", "", ""]);
    // Reset animations if going back
    setReverseCanvasVisible(false);
    setInitialCanvasVisible(true);
  };

  return (
    <div className={cn("flex w-[100%] flex-col min-h-screen bg-black relative", className)}>
      <div className="absolute inset-0 z-0">
        {/* Initial canvas (forward animation) */}
        {initialCanvasVisible && (
          <div className="absolute inset-0">
            <CanvasRevealEffect
              animationSpeed={3}
              containerClassName="bg-black"
              colors={[
                [255, 255, 255],
                [255, 255, 255],
              ]}
              dotSize={6}
              reverse={false}
            />
          </div>
        )}
        
        {/* Reverse canvas (appears when code is complete) */}
        {reverseCanvasVisible && (
          <div className="absolute inset-0">
            <CanvasRevealEffect
              animationSpeed={4}
              containerClassName="bg-black"
              colors={[
                [255, 255, 255],
                [255, 255, 255],
              ]}
              dotSize={6}
              reverse={true}
            />
          </div>
        )}
        
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(0,0,0,1)_0%,_transparent_100%)]" />
        <div className="absolute top-0 left-0 right-0 h-1/3 bg-gradient-to-b from-black to-transparent" />
      </div>
      
      {/* Content Layer */}
      <div className="relative z-10 flex flex-col flex-1">
        {/* Top navigation */}
        <MiniNavbar />

        {/* Main content container */}
        <div className="flex flex-1 flex-col lg:flex-row ">
          {/* Left side (form) */}
          <div className="flex-1 flex flex-col justify-center items-center">
            <div className="w-full mt-[150px] max-w-sm">
              <AnimatePresence mode="wait">
                {step === "email" ? (
                  <motion.div 
                    key="email-step"
                    initial={{ opacity: 0, x: -100 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -100 }}
                    transition={{ duration: 0.4, ease: "easeOut" }}
                    className="space-y-6 text-center"
                  >
                    <div className="space-y-1">
                      <h1 className="text-[2.5rem] font-bold leading-[1.1] tracking-tight text-white">Welcome Developer</h1>
                      <p className="text-[1.8rem] text-white/70 font-light">Your sign in component</p>
                    </div>
                    
                    
                    <div className="space-y-4">
                      <button className="backdrop-blur-[2px] w-full flex items-center justify-center gap-2 bg-white/5 hover:bg-white/10 text-white border border-white/10 rounded-full py-3 px-4 transition-colors">
                        <span className="text-lg">G</span>
                        <span>Sign in with Google</span>
                      </button>
                      
                      <div className="flex items-center gap-4">
                        <div className="h-px bg-white/10 flex-1" />
                        <span className="text-white/40 text-sm">or</span>
                        <div className="h-px bg-white/10 flex-1" />
                      </div>
                      
                      <form onSubmit={handleEmailSubmit}>
                        <div className="relative">
                          <input 
                            type="email" 
                            placeholder="info@gmail.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full backdrop-blur-[1px] text-white border-1 border-white/10 rounded-full py-3 px-4 focus:outline-none focus:border focus:border-white/30 text-center"
                            required
                          />
                          <button 
                            type="submit"
                            className="absolute right-1.5 top-1.5 text-white w-9 h-9 flex items-center justify-center rounded-full bg-white/10 hover:bg-white/20 transition-colors group overflow-hidden"
                          >
                            <span className="relative w-full h-full block overflow-hidden">
                              <span className="absolute inset-0 flex items-center justify-center transition-transform duration-300 group-hover:translate-x-full">
                                →
                              </span>
                              <span className="absolute inset-0 flex items-center justify-center transition-transform duration-300 -translate-x-full group-hover:translate-x-0">
                                →
                              </span>
                            </span>
                          </button>
                        </div>
                      </form>
                    </div>
                    
                    <p className="text-xs text-white/40 pt-10">
                      By signing up, you agree to the <Link href="#" className="underline text-white/40 hover:text-white/60 transition-colors">MSA</Link>, <Link href="#" className="underline text-white/40 hover:text-white/60 transition-colors">Product Terms</Link>, <Link href="#" className="underline text-white/40 hover:text-white/60 transition-colors">Policies</Link>, <Link href="#" className="underline text-white/40 hover:text-white/60 transition-colors">Privacy Notice</Link>, and <Link href="#" className="underline text-white/40 hover:text-white/60 transition-colors">Cookie Notice</Link>.
                    </p>
                  </motion.div>
                ) : step === "code" ? (
                  <motion.div 
                    key="code-step"
                    initial={{ opacity: 0, x: 100 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 100 }}
                    transition={{ duration: 0.4, ease: "easeOut" }}
                    className="space-y-6 text-center"
                  >
                    <div className="space-y-1">
                      <h1 className="text-[2.5rem] font-bold leading-[1.1] tracking-tight text-white">We sent you a code</h1>
                      <p className="text-[1.25rem] text-white/50 font-light">Please enter it</p>
                    </div>
                    
                    <div className="w-full">
                      <div className="relative rounded-full py-4 px-5 border border-white/10 bg-transparent">
                        <div className="flex items-center justify-center">
                          {code.map((digit, i) => (
                            <div key={i} className="flex items-center">
                              <div className="relative">
                                <input
                                  ref={(el) => {
                                    codeInputRefs.current[i] = el;
                                  }}
                                  type="text"
                                  inputMode="numeric"
                                  pattern="[0-9]*"
                                  maxLength={1}
                                  value={digit}
                                  onChange={e => handleCodeChange(i, e.target.value)}
                                  onKeyDown={e => handleKeyDown(i, e)}
                                  className="w-8 text-center text-xl bg-transparent text-white border-none focus:outline-none focus:ring-0 appearance-none"
                                  style={{ caretColor: 'transparent' }}
                                />
                                {!digit && (
                                  <div className="absolute top-0 left-0 w-full h-full flex items-center justify-center pointer-events-none">
                                    <span className="text-xl text-white">0</span>
                                  </div>
                                )}
                              </div>
                              {i < 5 && <span className="text-white/20 text-xl">|</span>}
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                    
                    <div>
                      <motion.p 
                        className="text-white/50 hover:text-white/70 transition-colors cursor-pointer text-sm"
                        whileHover={{ scale: 1.02 }}
                        transition={{ duration: 0.2 }}
                      >
                        Resend code
                      </motion.p>
                    </div>
                    
                    <div className="flex w-full gap-3">
                      <motion.button 
                        onClick={handleBackClick}
                        className="rounded-full bg-white text-black font-medium px-8 py-3 hover:bg-white/90 transition-colors w-[30%]"
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        transition={{ duration: 0.2 }}
                      >
                        Back
                      </motion.button>
                      <motion.button 
                        className={`flex-1 rounded-full font-medium py-3 border transition-all duration-300 ${
                          code.every(d => d !== "") 
                          ? "bg-white text-black border-transparent hover:bg-white/90 cursor-pointer" 
                          : "bg-[#111] text-white/50 border-white/10 cursor-not-allowed"
                        }`}
                        disabled={!code.every(d => d !== "")}
                      >
                        Continue
                      </motion.button>
                    </div>
                    
                    <div className="pt-16">
                      <p className="text-xs text-white/40">
                        By signing up, you agree to the <Link href="#" className="underline text-white/40 hover:text-white/60 transition-colors">MSA</Link>, <Link href="#" className="underline text-white/40 hover:text-white/60 transition-colors">Product Terms</Link>, <Link href="#" className="underline text-white/40 hover:text-white/60 transition-colors">Policies</Link>, <Link href="#" className="underline text-white/40 hover:text-white/60 transition-colors">Privacy Notice</Link>, and <Link href="#" className="underline text-white/40 hover:text-white/60 transition-colors">Cookie Notice</Link>.
                      </p>
                    </div>
                  </motion.div>
                ) : (
                  <motion.div 
                    key="success-step"
                    initial={{ opacity: 0, y: 50 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, ease: "easeOut", delay: 0.3 }}
                    className="space-y-6 text-center"
                  >
                    <div className="space-y-1">
                      <h1 className="text-[2.5rem] font-bold leading-[1.1] tracking-tight text-white">You're in!</h1>
                      <p className="text-[1.25rem] text-white/50 font-light">Welcome</p>
                    </div>
                    
                    <motion.div 
                      initial={{ scale: 0.8, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ duration: 0.5, delay: 0.5 }}
                      className="py-10"
                    >
                      <div className="mx-auto w-16 h-16 rounded-full bg-gradient-to-br from-white to-white/70 flex items-center justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-black" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      </div>
                    </motion.div>
                    
                    <motion.button 
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 1 }}
                      className="w-full rounded-full bg-white text-black font-medium py-3 hover:bg-white/90 transition-colors"
                    >
                      Continue to Dashboard
                    </motion.button>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
};



demo.tsx
import { SignInPage } from "@/components/ui/sign-in-flow-1";

const DemoOne = () => {
  return (
    <div className="flex w-full h-screen justify-center items-center">
      <SignInPage />
    </div>
  );
};

export { DemoOne };

```

Install NPM dependencies:
```bash
next, three, framer-motion, @react-three/fiber
```

Implementation Guidelines
 1. Analyze the component structure and identify all required dependencies
 2. Review the component's argumens and state
 3. Identify any required context providers or hooks and install them
 4. Questions to Ask
 - What data/props will be passed to this component?
 - Are there any specific state management requirements?
 - Are there any required assets (images, icons, etc.)?
 - What is the expected responsive behavior?
 - What is the best place to use this component in the app?

Steps to integrate
 0. Copy paste all the code above in the correct directories
 1. Install external dependencies
 2. Fill image assets with Unsplash stock images you know exist
 3. Use lucide-react icons for svgs or logos if component requires them


:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

You are given a task to integrate an existing React component in the codebase

The codebase should support:
- shadcn project structure  
- Tailwind CSS
- Typescript

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind or Typescript.

Determine the default path for components and styles. 
If default path for components is not /components/ui, provide instructions on why it's important to create this folder
Copy-paste this component to /components/ui folder:
```tsx
v0-ai-chat.tsx
"use client";

import { useEffect, useRef, useCallback } from "react";
import { useState } from "react";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";
import {
    ImageIcon,
    FileUp,
    Figma,
    MonitorIcon,
    CircleUserRound,
    ArrowUpIcon,
    Paperclip,
    PlusIcon,
} from "lucide-react";

interface UseAutoResizeTextareaProps {
    minHeight: number;
    maxHeight?: number;
}

function useAutoResizeTextarea({
    minHeight,
    maxHeight,
}: UseAutoResizeTextareaProps) {
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const adjustHeight = useCallback(
        (reset?: boolean) => {
            const textarea = textareaRef.current;
            if (!textarea) return;

            if (reset) {
                textarea.style.height = `${minHeight}px`;
                return;
            }

            // Temporarily shrink to get the right scrollHeight
            textarea.style.height = `${minHeight}px`;

            // Calculate new height
            const newHeight = Math.max(
                minHeight,
                Math.min(
                    textarea.scrollHeight,
                    maxHeight ?? Number.POSITIVE_INFINITY
                )
            );

            textarea.style.height = `${newHeight}px`;
        },
        [minHeight, maxHeight]
    );

    useEffect(() => {
        // Set initial height
        const textarea = textareaRef.current;
        if (textarea) {
            textarea.style.height = `${minHeight}px`;
        }
    }, [minHeight]);

    // Adjust height on window resize
    useEffect(() => {
        const handleResize = () => adjustHeight();
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, [adjustHeight]);

    return { textareaRef, adjustHeight };
}

export function VercelV0Chat() {
    const [value, setValue] = useState("");
    const { textareaRef, adjustHeight } = useAutoResizeTextarea({
        minHeight: 60,
        maxHeight: 200,
    });

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            if (value.trim()) {
                setValue("");
                adjustHeight(true);
            }
        }
    };

    return (
        <div className="flex flex-col items-center w-full max-w-4xl mx-auto p-4 space-y-8">
            <h1 className="text-4xl font-bold text-black dark:text-white">
                What can I help you ship?
            </h1>

            <div className="w-full">
                <div className="relative bg-neutral-900 rounded-xl border border-neutral-800">
                    <div className="overflow-y-auto">
                        <Textarea
                            ref={textareaRef}
                            value={value}
                            onChange={(e) => {
                                setValue(e.target.value);
                                adjustHeight();
                            }}
                            onKeyDown={handleKeyDown}
                            placeholder="Ask v0 a question..."
                            className={cn(
                                "w-full px-4 py-3",
                                "resize-none",
                                "bg-transparent",
                                "border-none",
                                "text-white text-sm",
                                "focus:outline-none",
                                "focus-visible:ring-0 focus-visible:ring-offset-0",
                                "placeholder:text-neutral-500 placeholder:text-sm",
                                "min-h-[60px]"
                            )}
                            style={{
                                overflow: "hidden",
                            }}
                        />
                    </div>

                    <div className="flex items-center justify-between p-3">
                        <div className="flex items-center gap-2">
                            <button
                                type="button"
                                className="group p-2 hover:bg-neutral-800 rounded-lg transition-colors flex items-center gap-1"
                            >
                                <Paperclip className="w-4 h-4 text-white" />
                                <span className="text-xs text-zinc-400 hidden group-hover:inline transition-opacity">
                                    Attach
                                </span>
                            </button>
                        </div>
                        <div className="flex items-center gap-2">
                            <button
                                type="button"
                                className="px-2 py-1 rounded-lg text-sm text-zinc-400 transition-colors border border-dashed border-zinc-700 hover:border-zinc-600 hover:bg-zinc-800 flex items-center justify-between gap-1"
                            >
                                <PlusIcon className="w-4 h-4" />
                                Project
                            </button>
                            <button
                                type="button"
                                className={cn(
                                    "px-1.5 py-1.5 rounded-lg text-sm transition-colors border border-zinc-700 hover:border-zinc-600 hover:bg-zinc-800 flex items-center justify-between gap-1",
                                    value.trim()
                                        ? "bg-white text-black"
                                        : "text-zinc-400"
                                )}
                            >
                                <ArrowUpIcon
                                    className={cn(
                                        "w-4 h-4",
                                        value.trim()
                                            ? "text-black"
                                            : "text-zinc-400"
                                    )}
                                />
                                <span className="sr-only">Send</span>
                            </button>
                        </div>
                    </div>
                </div>

                <div className="flex items-center justify-center gap-3 mt-4">
                    <ActionButton
                        icon={<ImageIcon className="w-4 h-4" />}
                        label="Clone a Screenshot"
                    />
                    <ActionButton
                        icon={<Figma className="w-4 h-4" />}
                        label="Import from Figma"
                    />
                    <ActionButton
                        icon={<FileUp className="w-4 h-4" />}
                        label="Upload a Project"
                    />
                    <ActionButton
                        icon={<MonitorIcon className="w-4 h-4" />}
                        label="Landing Page"
                    />
                    <ActionButton
                        icon={<CircleUserRound className="w-4 h-4" />}
                        label="Sign Up Form"
                    />
                </div>
            </div>
        </div>
    );
}

interface ActionButtonProps {
    icon: React.ReactNode;
    label: string;
}

function ActionButton({ icon, label }: ActionButtonProps) {
    return (
        <button
            type="button"
            className="flex items-center gap-2 px-4 py-2 bg-neutral-900 hover:bg-neutral-800 rounded-full border border-neutral-800 text-neutral-400 hover:text-white transition-colors"
        >
            {icon}
            <span className="text-xs">{label}</span>
        </button>
    );
}




demo.tsx
import { VercelV0Chat } from "@/components/ui/v0-ai-chat"

export function Demo() {
    return <VercelV0Chat />
}
```

Copy-paste these files for dependencies:
```tsx
shadcn/textarea
import * as React from "react"

import { cn } from "@/lib/utils"

export interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        className={cn(
          "flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Textarea.displayName = "Textarea"

export { Textarea }

```

Install NPM dependencies:
```bash
lucide-react
```

Implementation Guidelines
 1. Analyze the component structure and identify all required dependencies
 2. Review the component's argumens and state
 3. Identify any required context providers or hooks and install them
 4. Questions to Ask
 - What data/props will be passed to this component?
 - Are there any specific state management requirements?
 - Are there any required assets (images, icons, etc.)?
 - What is the expected responsive behavior?
 - What is the best place to use this component in the app?

Steps to integrate
 0. Copy paste all the code above in the correct directories
 1. Install external dependencies
 2. Fill image assets with Unsplash stock images you know exist
 3. Use lucide-react icons for svgs or logos if component requires them


:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

You are given a task to integrate an existing React component in the codebase

The codebase should support:
- shadcn project structure  
- Tailwind CSS
- Typescript

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind or Typescript.

Determine the default path for components and styles. 
If default path for components is not /components/ui, provide instructions on why it's important to create this folder
Copy-paste this component to /components/ui folder:
```tsx
map.tsx
"use client";

import { useRef, useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import DottedMap from "dotted-map";
import Image from "next/image";
import { useTheme } from "next-themes";

interface MapProps {
  dots?: Array<{
    start: { lat: number; lng: number; label?: string };
    end: { lat: number; lng: number; label?: string };
  }>;
  lineColor?: string;
  showLabels?: boolean;
  labelClassName?: string;
  animationDuration?: number;
  loop?: boolean;
}

export function WorldMap({ 
  dots = [], 
  lineColor = "#0ea5e9",
  showLabels = true,
  labelClassName = "text-sm",
  animationDuration = 2,
  loop = true
}: MapProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [hoveredLocation, setHoveredLocation] = useState<string | null>(null);
  const { theme } = useTheme();

  const map = useMemo(
    () => new DottedMap({ height: 100, grid: "diagonal" }),
    []
  );

  const svgMap = useMemo(
    () => map.getSVG({
      radius: 0.22,
      color: theme === "dark" ? "#FFFF7F40" : "#00000040",
      shape: "circle",
      backgroundColor: theme === "dark" ? "black" : "white",
    }),
    [map, theme]
  );

  const projectPoint = (lat: number, lng: number) => {
    const x = (lng + 180) * (800 / 360);
    const y = (90 - lat) * (400 / 180);
    return { x, y };
  };

  const createCurvedPath = (
    start: { x: number; y: number },
    end: { x: number; y: number }
  ) => {
    const midX = (start.x + end.x) / 2;
    const midY = Math.min(start.y, end.y) - 50;
    return `M ${start.x} ${start.y} Q ${midX} ${midY} ${end.x} ${end.y}`;
  };

  // Calculate animation timing
  const staggerDelay = 0.3;
  const totalAnimationTime = dots.length * staggerDelay + animationDuration;
  const pauseTime = 2; // Pause for 2 seconds when all paths are drawn
  const fullCycleDuration = totalAnimationTime + pauseTime;

  return (
    <div className="w-full aspect-[2/1] md:aspect-[2.5/1] lg:aspect-[2/1] dark:bg-black bg-white rounded-lg relative font-sans overflow-hidden">
      <Image
        src={`data:image/svg+xml;utf8,${encodeURIComponent(svgMap)}`}
        className="h-full w-full [mask-image:linear-gradient(to_bottom,transparent,white_10%,white_90%,transparent)] pointer-events-none select-none object-cover"
        alt="world map"
        height="495"
        width="1056"
        draggable={false}
        priority
      />
      <svg
        ref={svgRef}
        viewBox="0 0 800 400"
        className="w-full h-full absolute inset-0 pointer-events-auto select-none"
        preserveAspectRatio="xMidYMid meet"
      >
        <defs>
          <linearGradient id="path-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="white" stopOpacity="0" />
            <stop offset="5%" stopColor={lineColor} stopOpacity="1" />
            <stop offset="95%" stopColor={lineColor} stopOpacity="1" />
            <stop offset="100%" stopColor="white" stopOpacity="0" />
          </linearGradient>
          
          <filter id="glow">
            <feMorphology operator="dilate" radius="0.5" />
            <feGaussianBlur stdDeviation="1" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {dots.map((dot, i) => {
          const startPoint = projectPoint(dot.start.lat, dot.start.lng);
          const endPoint = projectPoint(dot.end.lat, dot.end.lng);
          
          // Calculate keyframe times for this specific path
          const startTime = (i * staggerDelay) / fullCycleDuration;
          const endTime = (i * staggerDelay + animationDuration) / fullCycleDuration;
          const resetTime = totalAnimationTime / fullCycleDuration;
          
          return (
            <g key={`path-group-${i}`}>
              <motion.path
                d={createCurvedPath(startPoint, endPoint)}
                fill="none"
                stroke="url(#path-gradient)"
                strokeWidth="1"
                initial={{ pathLength: 0 }}
                animate={loop ? {
                  pathLength: [0, 0, 1, 1, 0],
                } : {
                  pathLength: 1
                }}
                transition={loop ? {
                  duration: fullCycleDuration,
                  times: [0, startTime, endTime, resetTime, 1],
                  ease: "easeInOut",
                  repeat: Infinity,
                  repeatDelay: 0,
                } : {
                  duration: animationDuration,
                  delay: i * staggerDelay,
                  ease: "easeInOut",
                }}
              />
              
              {loop && (
                <motion.circle
                  r="4"
                  fill={lineColor}
                  initial={{ offsetDistance: "0%", opacity: 0 }}
                  animate={{
                    offsetDistance: [null, "0%", "100%", "100%", "100%"],
                    opacity: [0, 0, 1, 0, 0],
                  }}
                  transition={{
                    duration: fullCycleDuration,
                    times: [0, startTime, endTime, resetTime, 1],
                    ease: "easeInOut",
                    repeat: Infinity,
                    repeatDelay: 0,
                  }}
                  style={{
                    offsetPath: `path('${createCurvedPath(startPoint, endPoint)}')`,
                  }}
                />
              )}
            </g>
          );
        })}

        {dots.map((dot, i) => {
          const startPoint = projectPoint(dot.start.lat, dot.start.lng);
          const endPoint = projectPoint(dot.end.lat, dot.end.lng);
          
          return (
            <g key={`points-group-${i}`}>
              {/* Start Point */}
              <g key={`start-${i}`}>
                <motion.g
                  onHoverStart={() => setHoveredLocation(dot.start.label || `Location ${i}`)}
                  onHoverEnd={() => setHoveredLocation(null)}
                  className="cursor-pointer"
                  whileHover={{ scale: 1.2 }}
                  transition={{ type: "spring", stiffness: 400, damping: 10 }}
                >
                  <circle
                    cx={startPoint.x}
                    cy={startPoint.y}
                    r="3"
                    fill={lineColor}
                    filter="url(#glow)"
                    className="drop-shadow-lg"
                  />
                  <circle
                    cx={startPoint.x}
                    cy={startPoint.y}
                    r="3"
                    fill={lineColor}
                    opacity="0.5"
                  >
                    <animate
                      attributeName="r"
                      from="3"
                      to="12"
                      dur="2s"
                      begin="0s"
                      repeatCount="indefinite"
                    />
                    <animate
                      attributeName="opacity"
                      from="0.6"
                      to="0"
                      dur="2s"
                      begin="0s"
                      repeatCount="indefinite"
                    />
                  </circle>
                </motion.g>
                
                {showLabels && dot.start.label && (
                  <motion.g
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 * i + 0.3, duration: 0.5 }}
                    className="pointer-events-none"
                  >
                    <foreignObject
                      x={startPoint.x - 50}
                      y={startPoint.y - 35}
                      width="100"
                      height="30"
                      className="block"
                    >
                      <div className="flex items-center justify-center h-full">
                        <span className="text-sm font-medium px-2 py-0.5 rounded-md bg-white/95 dark:bg-black/95 text-black dark:text-white border border-gray-200 dark:border-gray-700 shadow-sm">
                          {dot.start.label}
                        </span>
                      </div>
                    </foreignObject>
                  </motion.g>
                )}
              </g>
              
              {/* End Point */}
              <g key={`end-${i}`}>
                <motion.g
                  onHoverStart={() => setHoveredLocation(dot.end.label || `Destination ${i}`)}
                  onHoverEnd={() => setHoveredLocation(null)}
                  className="cursor-pointer"
                  whileHover={{ scale: 1.2 }}
                  transition={{ type: "spring", stiffness: 400, damping: 10 }}
                >
                  <circle
                    cx={endPoint.x}
                    cy={endPoint.y}
                    r="3"
                    fill={lineColor}
                    filter="url(#glow)"
                    className="drop-shadow-lg"
                  />
                  <circle
                    cx={endPoint.x}
                    cy={endPoint.y}
                    r="3"
                    fill={lineColor}
                    opacity="0.5"
                  >
                    <animate
                      attributeName="r"
                      from="3"
                      to="12"
                      dur="2s"
                      begin="0.5s"
                      repeatCount="indefinite"
                    />
                    <animate
                      attributeName="opacity"
                      from="0.6"
                      to="0"
                      dur="2s"
                      begin="0.5s"
                      repeatCount="indefinite"
                    />
                  </circle>
                </motion.g>
                
                {showLabels && dot.end.label && (
                  <motion.g
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 * i + 0.5, duration: 0.5 }}
                    className="pointer-events-none"
                  >
                    <foreignObject
                      x={endPoint.x - 50}
                      y={endPoint.y - 35}
                      width="100"
                      height="30"
                      className="block"
                    >
                      <div className="flex items-center justify-center h-full">
                        <span className="text-sm font-medium px-2 py-0.5 rounded-md bg-white/95 dark:bg-black/95 text-black dark:text-white border border-gray-200 dark:border-gray-700 shadow-sm">
                          {dot.end.label}
                        </span>
                      </div>
                    </foreignObject>
                  </motion.g>
                )}
              </g>
            </g>
          );
        })}
      </svg>
      
      {/* Mobile Tooltip */}
      <AnimatePresence>
        {hoveredLocation && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="absolute bottom-4 left-4 bg-white/90 dark:bg-black/90 text-black dark:text-white px-3 py-2 rounded-lg text-sm font-medium backdrop-blur-sm sm:hidden border border-gray-200 dark:border-gray-700"
          >
            {hoveredLocation}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

demo.tsx
"use client";
import { WorldMap } from "@/components/ui/map";
import { motion } from "framer-motion";

export default function MapDemo() {
  return (
    <div className=" py-40 dark:bg-black bg-white w-full">
      <div className="max-w-7xl mx-auto text-center">
       <p className="font-bold text-xl md:text-4xl dark:text-white text-black">
          Global{" "}
         Network
        </p>
        <p className="text-sm md:text-lg text-neutral-500 max-w-2xl mx-auto py-4">
          Connect with teams and clients worldwide. Our platform enables seamless 
          collaboration across continents, bringing the world to your workspace.
        </p>
      </div>
      <WorldMap
        dots={[
          {
            start: {
              lat: 64.2008,
              lng: -149.4937,
              label: "Fairbanks"
            },
            end: {
              lat: 34.0522,
              lng: -118.2437,
              label: "Los Angeles"
            },
          },
          {
            start: { 
              lat: 64.2008, 
              lng: -149.4937,
              label: "Fairbanks"
            },
            end: { 
              lat: -15.7975, 
              lng: -47.8919,
              label: "Brasília"
            },
          },
          {
            start: { 
              lat: -15.7975, 
              lng: -47.8919,
              label: "Brasília"
            },
            end: { 
              lat: 38.7223, 
              lng: -9.1393,
              label: "Lisbon"
            },
          },
          {
            start: { 
              lat: 51.5074, 
              lng: -0.1278,
              label: "London"
            },
            end: { 
              lat: 28.6139, 
              lng: 77.209,
              label: "New Delhi"
            },
          },
          {
            start: { 
              lat: 28.6139, 
              lng: 77.209,
              label: "New Delhi"
            },
            end: { 
              lat: 43.1332, 
              lng: 131.9113,
              label: "Vladivostok"
            },
          },
          {
            start: { 
              lat: 28.6139, 
              lng: 77.209,
              label: "New Delhi"
            },
            end: { 
              lat: -1.2921, 
              lng: 36.8219,
              label: "Nairobi"
            },
          },
        ]}
      />
    </div>
  );
}

```

Install NPM dependencies:
```bash
next, dotted-map, next-themes, framer-motion
```

Implementation Guidelines
 1. Analyze the component structure and identify all required dependencies
 2. Review the component's argumens and state
 3. Identify any required context providers or hooks and install them
 4. Questions to Ask
 - What data/props will be passed to this component?
 - Are there any specific state management requirements?
 - Are there any required assets (images, icons, etc.)?
 - What is the expected responsive behavior?
 - What is the best place to use this component in the app?

Steps to integrate
 0. Copy paste all the code above in the correct directories
 1. Install external dependencies
 2. Fill image assets with Unsplash stock images you know exist
 3. Use lucide-react icons for svgs or logos if component requires them

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

You are given a task to integrate an existing React component in the codebase

The codebase should support:
- shadcn project structure  
- Tailwind CSS
- Typescript

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind or Typescript.

Determine the default path for components and styles. 
If default path for components is not /components/ui, provide instructions on why it's important to create this folder
Copy-paste this component to /components/ui folder:
```tsx
scroll-expansion-hero.tsx
'use client';

import {
  useEffect,
  useRef,
  useState,
  ReactNode,
  TouchEvent,
  WheelEvent,
} from 'react';
import Image from 'next/image';
import { motion } from 'framer-motion';

interface ScrollExpandMediaProps {
  mediaType?: 'video' | 'image';
  mediaSrc: string;
  posterSrc?: string;
  bgImageSrc: string;
  title?: string;
  date?: string;
  scrollToExpand?: string;
  textBlend?: boolean;
  children?: ReactNode;
}

const ScrollExpandMedia = ({
  mediaType = 'video',
  mediaSrc,
  posterSrc,
  bgImageSrc,
  title,
  date,
  scrollToExpand,
  textBlend,
  children,
}: ScrollExpandMediaProps) => {
  const [scrollProgress, setScrollProgress] = useState<number>(0);
  const [showContent, setShowContent] = useState<boolean>(false);
  const [mediaFullyExpanded, setMediaFullyExpanded] = useState<boolean>(false);
  const [touchStartY, setTouchStartY] = useState<number>(0);
  const [isMobileState, setIsMobileState] = useState<boolean>(false);

  const sectionRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    setScrollProgress(0);
    setShowContent(false);
    setMediaFullyExpanded(false);
  }, [mediaType]);

  useEffect(() => {
    const handleWheel = (e: WheelEvent) => {
      if (mediaFullyExpanded && e.deltaY < 0 && window.scrollY <= 5) {
        setMediaFullyExpanded(false);
        e.preventDefault();
      } else if (!mediaFullyExpanded) {
        e.preventDefault();
        const scrollDelta = e.deltaY * 0.0009;
        const newProgress = Math.min(
          Math.max(scrollProgress + scrollDelta, 0),
          1
        );
        setScrollProgress(newProgress);

        if (newProgress >= 1) {
          setMediaFullyExpanded(true);
          setShowContent(true);
        } else if (newProgress < 0.75) {
          setShowContent(false);
        }
      }
    };

    const handleTouchStart = (e: TouchEvent) => {
      setTouchStartY(e.touches[0].clientY);
    };

    const handleTouchMove = (e: TouchEvent) => {
      if (!touchStartY) return;

      const touchY = e.touches[0].clientY;
      const deltaY = touchStartY - touchY;

      if (mediaFullyExpanded && deltaY < -20 && window.scrollY <= 5) {
        setMediaFullyExpanded(false);
        e.preventDefault();
      } else if (!mediaFullyExpanded) {
        e.preventDefault();
        // Increase sensitivity for mobile, especially when scrolling back
        const scrollFactor = deltaY < 0 ? 0.008 : 0.005; // Higher sensitivity for scrolling back
        const scrollDelta = deltaY * scrollFactor;
        const newProgress = Math.min(
          Math.max(scrollProgress + scrollDelta, 0),
          1
        );
        setScrollProgress(newProgress);

        if (newProgress >= 1) {
          setMediaFullyExpanded(true);
          setShowContent(true);
        } else if (newProgress < 0.75) {
          setShowContent(false);
        }

        setTouchStartY(touchY);
      }
    };

    const handleTouchEnd = (): void => {
      setTouchStartY(0);
    };

    const handleScroll = (): void => {
      if (!mediaFullyExpanded) {
        window.scrollTo(0, 0);
      }
    };

    window.addEventListener('wheel', handleWheel as unknown as EventListener, {
      passive: false,
    });
    window.addEventListener('scroll', handleScroll as EventListener);
    window.addEventListener(
      'touchstart',
      handleTouchStart as unknown as EventListener,
      { passive: false }
    );
    window.addEventListener(
      'touchmove',
      handleTouchMove as unknown as EventListener,
      { passive: false }
    );
    window.addEventListener('touchend', handleTouchEnd as EventListener);

    return () => {
      window.removeEventListener(
        'wheel',
        handleWheel as unknown as EventListener
      );
      window.removeEventListener('scroll', handleScroll as EventListener);
      window.removeEventListener(
        'touchstart',
        handleTouchStart as unknown as EventListener
      );
      window.removeEventListener(
        'touchmove',
        handleTouchMove as unknown as EventListener
      );
      window.removeEventListener('touchend', handleTouchEnd as EventListener);
    };
  }, [scrollProgress, mediaFullyExpanded, touchStartY]);

  useEffect(() => {
    const checkIfMobile = (): void => {
      setIsMobileState(window.innerWidth < 768);
    };

    checkIfMobile();
    window.addEventListener('resize', checkIfMobile);

    return () => window.removeEventListener('resize', checkIfMobile);
  }, []);

  const mediaWidth = 300 + scrollProgress * (isMobileState ? 650 : 1250);
  const mediaHeight = 400 + scrollProgress * (isMobileState ? 200 : 400);
  const textTranslateX = scrollProgress * (isMobileState ? 180 : 150);

  const firstWord = title ? title.split(' ')[0] : '';
  const restOfTitle = title ? title.split(' ').slice(1).join(' ') : '';

  return (
    <div
      ref={sectionRef}
      className='transition-colors duration-700 ease-in-out overflow-x-hidden'
    >
      <section className='relative flex flex-col items-center justify-start min-h-[100dvh]'>
        <div className='relative w-full flex flex-col items-center min-h-[100dvh]'>
          <motion.div
            className='absolute inset-0 z-0 h-full'
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 - scrollProgress }}
            transition={{ duration: 0.1 }}
          >
            <Image
              src={bgImageSrc}
              alt='Background'
              width={1920}
              height={1080}
              className='w-screen h-screen'
              style={{
                objectFit: 'cover',
                objectPosition: 'center',
              }}
              priority
            />
            <div className='absolute inset-0 bg-black/10' />
          </motion.div>

          <div className='container mx-auto flex flex-col items-center justify-start relative z-10'>
            <div className='flex flex-col items-center justify-center w-full h-[100dvh] relative'>
              <div
                className='absolute z-0 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 transition-none rounded-2xl'
                style={{
                  width: `${mediaWidth}px`,
                  height: `${mediaHeight}px`,
                  maxWidth: '95vw',
                  maxHeight: '85vh',
                  boxShadow: '0px 0px 50px rgba(0, 0, 0, 0.3)',
                }}
              >
                {mediaType === 'video' ? (
                  mediaSrc.includes('youtube.com') ? (
                    <div className='relative w-full h-full pointer-events-none'>
                      <iframe
                        width='100%'
                        height='100%'
                        src={
                          mediaSrc.includes('embed')
                            ? mediaSrc +
                              (mediaSrc.includes('?') ? '&' : '?') +
                              'autoplay=1&mute=1&loop=1&controls=0&showinfo=0&rel=0&disablekb=1&modestbranding=1'
                            : mediaSrc.replace('watch?v=', 'embed/') +
                              '?autoplay=1&mute=1&loop=1&controls=0&showinfo=0&rel=0&disablekb=1&modestbranding=1&playlist=' +
                              mediaSrc.split('v=')[1]
                        }
                        className='w-full h-full rounded-xl'
                        frameBorder='0'
                        allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'
                        allowFullScreen
                      />
                      <div
                        className='absolute inset-0 z-10'
                        style={{ pointerEvents: 'none' }}
                      ></div>

                      <motion.div
                        className='absolute inset-0 bg-black/30 rounded-xl'
                        initial={{ opacity: 0.7 }}
                        animate={{ opacity: 0.5 - scrollProgress * 0.3 }}
                        transition={{ duration: 0.2 }}
                      />
                    </div>
                  ) : (
                    <div className='relative w-full h-full pointer-events-none'>
                      <video
                        src={mediaSrc}
                        poster={posterSrc}
                        autoPlay
                        muted
                        loop
                        playsInline
                        preload='auto'
                        className='w-full h-full object-cover rounded-xl'
                        controls={false}
                        disablePictureInPicture
                        disableRemotePlayback
                      />
                      <div
                        className='absolute inset-0 z-10'
                        style={{ pointerEvents: 'none' }}
                      ></div>

                      <motion.div
                        className='absolute inset-0 bg-black/30 rounded-xl'
                        initial={{ opacity: 0.7 }}
                        animate={{ opacity: 0.5 - scrollProgress * 0.3 }}
                        transition={{ duration: 0.2 }}
                      />
                    </div>
                  )
                ) : (
                  <div className='relative w-full h-full'>
                    <Image
                      src={mediaSrc}
                      alt={title || 'Media content'}
                      width={1280}
                      height={720}
                      className='w-full h-full object-cover rounded-xl'
                    />

                    <motion.div
                      className='absolute inset-0 bg-black/50 rounded-xl'
                      initial={{ opacity: 0.7 }}
                      animate={{ opacity: 0.7 - scrollProgress * 0.3 }}
                      transition={{ duration: 0.2 }}
                    />
                  </div>
                )}

                <div className='flex flex-col items-center text-center relative z-10 mt-4 transition-none'>
                  {date && (
                    <p
                      className='text-2xl text-blue-200'
                      style={{ transform: `translateX(-${textTranslateX}vw)` }}
                    >
                      {date}
                    </p>
                  )}
                  {scrollToExpand && (
                    <p
                      className='text-blue-200 font-medium text-center'
                      style={{ transform: `translateX(${textTranslateX}vw)` }}
                    >
                      {scrollToExpand}
                    </p>
                  )}
                </div>
              </div>

              <div
                className={`flex items-center justify-center text-center gap-4 w-full relative z-10 transition-none flex-col ${
                  textBlend ? 'mix-blend-difference' : 'mix-blend-normal'
                }`}
              >
                <motion.h2
                  className='text-4xl md:text-5xl lg:text-6xl font-bold text-blue-200 transition-none'
                  style={{ transform: `translateX(-${textTranslateX}vw)` }}
                >
                  {firstWord}
                </motion.h2>
                <motion.h2
                  className='text-4xl md:text-5xl lg:text-6xl font-bold text-center text-blue-200 transition-none'
                  style={{ transform: `translateX(${textTranslateX}vw)` }}
                >
                  {restOfTitle}
                </motion.h2>
              </div>
            </div>

            <motion.section
              className='flex flex-col w-full px-8 py-10 md:px-16 lg:py-20'
              initial={{ opacity: 0 }}
              animate={{ opacity: showContent ? 1 : 0 }}
              transition={{ duration: 0.7 }}
            >
              {children}
            </motion.section>
          </div>
        </div>
      </section>
    </div>
  );
};

export default ScrollExpandMedia;


demo.tsx
'use client';

import { useState, useEffect } from 'react';
import ScrollExpandMedia from '@/components/blocks/scroll-expansion-hero';

interface MediaAbout {
  overview: string;
  conclusion: string;
}

interface MediaContent {
  src: string;
  poster?: string;
  background: string;
  title: string;
  date: string;
  scrollToExpand: string;
  about: MediaAbout;
}

interface MediaContentCollection {
  [key: string]: MediaContent;
}

const sampleMediaContent: MediaContentCollection = {
  video: {
    src: 'https://me7aitdbxq.ufs.sh/f/2wsMIGDMQRdYuZ5R8ahEEZ4aQK56LizRdfBSqeDMsmUIrJN1',
    poster:
      'https://images.pexels.com/videos/5752729/space-earth-universe-cosmos-5752729.jpeg',
    background:
      'https://me7aitdbxq.ufs.sh/f/2wsMIGDMQRdYMNjMlBUYHaeYpxduXPVNwf8mnFA61L7rkcoS',
    title: 'Immersive Video Experience',
    date: 'Cosmic Journey',
    scrollToExpand: 'Scroll to Expand Demo',
    about: {
      overview:
        'This is a demonstration of the ScrollExpandMedia component with a video. As you scroll, the video expands to fill more of the screen, creating an immersive experience. This component is perfect for showcasing video content in a modern, interactive way.',
      conclusion:
        'The ScrollExpandMedia component provides a unique way to engage users with your content through interactive scrolling. Try switching between video and image modes to see different implementations.',
    },
  },
  image: {
    src: 'https://images.unsplash.com/photo-1682687982501-1e58ab814714?q=80&w=1280&auto=format&fit=crop',
    background:
      'https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1920&auto=format&fit=crop',
    title: 'Dynamic Image Showcase',
    date: 'Underwater Adventure',
    scrollToExpand: 'Scroll to Expand Demo',
    about: {
      overview:
        'This is a demonstration of the ScrollExpandMedia component with an image. The same smooth expansion effect works beautifully with static images, allowing you to create engaging visual experiences without video content.',
      conclusion:
        'The ScrollExpandMedia component works equally well with images and videos. This flexibility allows you to choose the media type that best suits your content while maintaining the same engaging user experience.',
    },
  },
};

const MediaContent = ({ mediaType }: { mediaType: 'video' | 'image' }) => {
  const currentMedia = sampleMediaContent[mediaType];

  return (
    <div className='max-w-4xl mx-auto'>
      <h2 className='text-3xl font-bold mb-6 text-black dark:text-white'>
        About This Component
      </h2>
      <p className='text-lg mb-8 text-black dark:text-white'>
        {currentMedia.about.overview}
      </p>

      <p className='text-lg mb-8 text-black dark:text-white'>
        {currentMedia.about.conclusion}
      </p>
    </div>
  );
};

export const VideoExpansionTextBlend = () => {
  const mediaType = 'video';
  const currentMedia = sampleMediaContent[mediaType];

  useEffect(() => {
    window.scrollTo(0, 0);

    const resetEvent = new Event('resetSection');
    window.dispatchEvent(resetEvent);
  }, []);

  return (
    <div className='min-h-screen'>
      <ScrollExpandMedia
        mediaType={mediaType}
        mediaSrc={currentMedia.src}
        posterSrc={currentMedia.poster}
        bgImageSrc={currentMedia.background}
        title={currentMedia.title}
        date={currentMedia.date}
        scrollToExpand={currentMedia.scrollToExpand}
        textBlend
      >
        <MediaContent mediaType={mediaType} />
      </ScrollExpandMedia>
    </div>
  );
};

export const ImageExpansionTextBlend = () => {
  const mediaType = 'image';
  const currentMedia = sampleMediaContent[mediaType];

  useEffect(() => {
    window.scrollTo(0, 0);

    const resetEvent = new Event('resetSection');
    window.dispatchEvent(resetEvent);
  }, []);

  return (
    <div className='min-h-screen'>
      <ScrollExpandMedia
        mediaType={mediaType}
        mediaSrc={currentMedia.src}
        bgImageSrc={currentMedia.background}
        title={currentMedia.title}
        date={currentMedia.date}
        scrollToExpand={currentMedia.scrollToExpand}
        textBlend
      >
        <MediaContent mediaType={mediaType} />
      </ScrollExpandMedia>
    </div>
  );
};

export const VideoExpansion = () => {
  const mediaType = 'video';
  const currentMedia = sampleMediaContent[mediaType];

  useEffect(() => {
    window.scrollTo(0, 0);

    const resetEvent = new Event('resetSection');
    window.dispatchEvent(resetEvent);
  }, []);

  return (
    <div className='min-h-screen'>
      <ScrollExpandMedia
        mediaType={mediaType}
        mediaSrc={currentMedia.src}
        posterSrc={currentMedia.poster}
        bgImageSrc={currentMedia.background}
        title={currentMedia.title}
        date={currentMedia.date}
        scrollToExpand={currentMedia.scrollToExpand}
      >
        <MediaContent mediaType={mediaType} />
      </ScrollExpandMedia>
    </div>
  );
};

export const ImageExpansion = () => {
  const mediaType = 'image';
  const currentMedia = sampleMediaContent[mediaType];

  useEffect(() => {
    window.scrollTo(0, 0);

    const resetEvent = new Event('resetSection');
    window.dispatchEvent(resetEvent);
  }, []);

  return (
    <div className='min-h-screen'>
      <ScrollExpandMedia
        mediaType={mediaType}
        mediaSrc={currentMedia.src}
        bgImageSrc={currentMedia.background}
        title={currentMedia.title}
        date={currentMedia.date}
        scrollToExpand={currentMedia.scrollToExpand}
      >
        <MediaContent mediaType={mediaType} />
      </ScrollExpandMedia>
    </div>
  );
};

const Demo = () => {
  const [mediaType, setMediaType] = useState('video');
  const currentMedia = sampleMediaContent[mediaType];

  useEffect(() => {
    window.scrollTo(0, 0);

    const resetEvent = new Event('resetSection');
    window.dispatchEvent(resetEvent);
  }, [mediaType]);

  return (
    <div className='min-h-screen'>
      <div className='fixed top-4 right-4 z-50 flex gap-2'>
        <button
          onClick={() => setMediaType('video')}
          className={`px-4 py-2 rounded-lg ${
            mediaType === 'video'
              ? 'bg-white text-black'
              : 'bg-black/50 text-white border border-white/30'
          }`}
        >
          Video
        </button>

        <button
          onClick={() => setMediaType('image')}
          className={`px-4 py-2 rounded-lg ${
            mediaType === 'image'
              ? 'bg-white text-black'
              : 'bg-black/50 text-white border border-white/30'
          }`}
        >
          Image
        </button>
      </div>

      <ScrollExpandMedia
        mediaType={mediaType as 'video' | 'image'}
        mediaSrc={currentMedia.src}
        posterSrc={mediaType === 'video' ? currentMedia.poster : undefined}
        bgImageSrc={currentMedia.background}
        title={currentMedia.title}
        date={currentMedia.date}
        scrollToExpand={currentMedia.scrollToExpand}
      >
        <MediaContent mediaType={mediaType as 'video' | 'image'} />
      </ScrollExpandMedia>
    </div>
  );
};

export default Demo;

```

Install NPM dependencies:
```bash
framer-motion
```

Implementation Guidelines
 1. Analyze the component structure and identify all required dependencies
 2. Review the component's argumens and state
 3. Identify any required context providers or hooks and install them
 4. Questions to Ask
 - What data/props will be passed to this component?
 - Are there any specific state management requirements?
 - Are there any required assets (images, icons, etc.)?
 - What is the expected responsive behavior?
 - What is the best place to use this component in the app?

Steps to integrate
 0. Copy paste all the code above in the correct directories
 1. Install external dependencies
 2. Fill image assets with Unsplash stock images you know exist
 3. Use lucide-react icons for svgs or logos if component requires them

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::;;

You are given a task to integrate an existing React component in the codebase

The codebase should support:
- shadcn project structure  
- Tailwind CSS
- Typescript

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind or Typescript.

Determine the default path for components and styles. 
If default path for components is not /components/ui, provide instructions on why it's important to create this folder
Copy-paste this component to /components/ui folder:
```tsx
siri-wave.tsx
"use client"

import * as React from "react"

import { cn } from "@/lib/utils"

/**
 * Siri-style GLSL shaders rendered on a raw WebGL canvas.
 *
 * - `"wave"`        — the iOS voice waveform (chromatic, frequency-reactive).
 * - `"fluid-dots"`  — six metaball dots that merge, scatter and gather.
 *
 * Self-contained: a single fullscreen triangle drives a fragment shader, no
 * external WebGL library. The shaders are ported verbatim from the original
 * `siriWaveCore` / `siriFluidDotsCore` sources.
 */

export type SiriWaveVariant = "wave" | "fluid-dots"

const VERTEX_SHADER = `attribute vec2 aPos; void main(){ gl_Position=vec4(aPos,0.0,1.0); }`

const WAVE_SHADER = `precision highp float;
uniform vec2 iResolution; uniform float iTime;
const float PI = 3.14159265359;
const float AMPLITUDE   = 0.32;
const float FREQ        = 1.1;
const float ABER_FREQ   = 1.0;
const float SPEED       = 2.4;
const float WAVE_SCALE  = 0.6;
const float ABERRATION  = 2.6;
const float THICKNESS   = 3.0;
const float INTENSITY   = 2.;
const float FALLOFF     = 1.7;
const float EDGE_MASK   = 0.4;
const float EDGE_INSET  = 0.0;
const float BAND_FILL   = 30000.0;
const float BAND_THICK  = 0.08;
const float SOFTNESS    = 2.5;
const float LOW_AMP     = 6.0;
const float LOW_INT     = 1.5;
const float MID_ABER    = 0.8;
const float MID_ABAMP   = 0.05;
const float MID_BAND    = 20.0;
const float MID_SOFT    = 0.4;
const float HIGH_ABER   = 0.5;
const float HIGH_ABAMP  = 0.06;
const float RESOLVED    = 1.0;
const float UNRES_SCALE = 0.14;

vec3 spectral4(int s){
    float x = float(s);
    return clamp(vec3(abs(x-3.0)-1.0, 2.0-abs(x-2.0), 2.0-abs(x-4.0)), 0.0, 1.0);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord){
    vec2 R = iResolution.xy;
    float aspect = R.x / R.y;
    vec2 p = (fragCoord + 0.5) * 2.0 / R - 1.0;
    p.x *= aspect;
    float yScreen = p.y;
    p /= max(WAVE_SCALE, 0.1);

    float t   = iTime;
    float low  = clamp(0.45 + 0.45*sin(t*0.8)*sin(t*0.37+1.0), 0.0, 1.0);
    float mid  = clamp(0.40 + 0.40*sin(t*1.7+2.0)*sin(t*0.53), 0.0, 1.0);
    float high = clamp(0.30 + 0.30*sin(t*2.9+4.0)*sin(t*0.71+2.0), 0.0, 1.0);

    float res   = clamp(RESOLVED, 0.0, 1.0);
    float drift = mod(t, 20.0*PI) * SPEED;

    float xN  = p.x / max(aspect, 1.0);
    float env = cos(PI*0.5 * min(abs(0.9*xN), 1.0));
    env *= env;

    float A1    = AMPLITUDE + 0.01*low*LOW_AMP;
    float A2    = A1 + mid*MID_ABAMP + high*HIGH_ABAMP;
    float AB    = (ABERRATION + mid*MID_ABER + high*HIGH_ABER)*res;
    float th    = mix(0.1, 0.01*THICKNESS, res);
    float inten = mix(0.1, 0.01*(INTENSITY + low*LOW_INT), res);
    float soft  = 0.01*res*max(0.0, SOFTNESS + mid*MID_SOFT);

    float dUnres = max(length(p) - mix(0.14, UNRES_SCALE, res), 0.0);
    float yMain = A1 * env * res * sin(p.x*FREQ + drift);

    float bandFillTh = max(BAND_THICK, 1e-4);
    float bandAmt    = 1e-4 * BAND_FILL * inten;
    vec3 num = vec3(0.0), den = vec3(0.0);
    for(int s = 0; s < 4; s++){
        vec3 hue = mix(vec3(1.0), spectral4(s), res);
        den += hue;
        float ab = mix(-AB, AB, float(s)/3.0);
        float yL = A2 * env * res * sin(p.x*ABER_FREQ + drift + ab);
        float d   = mix(dUnres, abs(p.y - yL), res);
        float lor = mix(1.0/(1.0 + (0.02*d)*(0.02*d)), 1.0, res);
        float line = inten / (sqrt(d*d + soft*soft) + th);
        float lo = min(yMain, yL), hi = max(yMain, yL);
        float dBand = max(0.0, max(p.y - hi, lo - p.y));
        float band  = bandAmt / (dBand + bandFillTh);
        num += hue * lor * (line + band);
    }
    vec3 col = num / den;

    float dM    = mix(dUnres, abs(p.y - yMain), res);
    float lorM  = mix(1.0/(1.0 + (0.02*dM)*(0.02*dM)), 1.0, res);
    float boost = (1.0 - res) * (14.0*low + 4.0);
    col += 0.5 * inten * (lorM + boost) / (sqrt(dM*dM + soft*soft) + th);

    col = pow(max(col, 0.0), vec3(1.5));
    float emT = clamp((abs(yScreen) - 1.0 + EDGE_INSET) / (-max(EDGE_MASK, 1e-4)), 0.0, 1.0);
    float em  = emT*emT*(3.0 - 2.0*emT);
    float gauss = exp(-pow(xN*FALLOFF, 2.0));
    col *= mix(1.0, em*gauss, res);
    col *= res;
    fragColor = vec4(col, 1.0);
}
void main(){ mainImage(gl_FragColor, gl_FragCoord.xy); }`

const FLUID_DOTS_SHADER = `precision highp float;
uniform vec2 iResolution; uniform float iTime;
const float TAU = 6.28318530718;
const int   N   = 6;
const float SMOOTH_K = 0.08;
const float INTENSITY  = 0.0025;
const float FALLOFF_P  = 1.35;
const float FADE_START = 0.02;
const float FADE_END   = 0.56;
const float ABERR = 0.005;
const vec3  SPECTRAL = vec3(0.0, 0.5, 1.0) * ABERR;
const float HUE_SPEED = 0.06;
const float COLOR_K   = 0.5;
const float SAT       = 0.01;
const float HUE_SPAN  = 0.667;
const float MERGE_PERIOD = 6.0;
const float T_MOVE   = 1.25;
const float STAGGER  = 0.33;
const float HOLD     = 0.0;
const float W = 4.6;
const float L = 3.2;
const float PIERCE  = 0.12;
const float RECOIL  = 0.035;
const float REC_LAG = 0.11;
const float GATHER_PERIOD = 12.0;
const float GATHER_START  = 9.2;
const float GATHER_HOLD   = 0.8;
const float GATHER_R      = 0.008;
const float GATHER_DIM    = 0.85;
const float GATHER_IN     = 1.8;
const float GATHER_IN_L   = 7.5;
const float BURST_W = 6.5;
const float BURST_L = 4.0;
const float CHARGE_T     = 0.30;
const float CHARGE_SHRK  = 0.18;
const float CHARGE_GLOW  = 0.35;
const float FLASH_GAIN   = 1.2;
const float FLASH_DECAY  = 7.0;

float hash11(float n){ return fract(sin(n*127.1 + 311.7)*43758.5453); }
float settleWL(float tau, float w, float l){
    if(tau <= 0.0) return 0.0;
    return 1.0 - exp(-l*tau)*cos(w*tau);
}
float settle(float tau){ return settleWL(tau, W, L); }
float settleCrit(float tau, float l){
    if(tau <= 0.0) return 0.0;
    return 1.0 - exp(-l*tau)*(1.0 + l*tau);
}
float smin(float a, float b, float k){
    float h = max(k - abs(a - b), 0.0) / k;
    return min(a, b) - h*h*k*0.25;
}
vec3 hue2rgb(float h){
    h = fract(h);
    float r = clamp(abs(h*6.0 - 3.0) - 1.0, 0.0, 1.0);
    float g = clamp(2.0 - abs(h*6.0 - 2.0), 0.0, 1.0);
    float b = clamp(2.0 - abs(h*6.0 - 4.0), 0.0, 1.0);
    return vec3(r, g, b);
}
float dotR(float fi, float seed, float t){
    return 0.036 + 0.010*sin(t*1.3 + seed*TAU) + 0.005*sin(t*2.4 + fi*1.3);
}
float dotSD(vec2 p, vec2 pos, float r, float t, float fi, float shapeDamp){
    vec2 d = p - pos;
    float sq = 0.075 * (0.5 + 0.5*sin(t*0.9 + fi*2.0)) * shapeDamp;
    float ca = cos(t*0.35 + fi), sa = sin(t*0.35 + fi);
    d = mat2(ca,-sa,sa,ca) * d;
    d *= vec2(1.0+sq, 1.0-sq);
    return length(d) - r;
}
vec3 scene(vec2 p, float t){
    float k  = floor(t/MERGE_PERIOD);
    float u  = fract(t/MERGE_PERIOD);
    float te = u * MERGE_PERIOD;
    float tg = mod(t, GATHER_PERIOD);
    float g  = settleCrit((tg - GATHER_START) * GATHER_IN, GATHER_IN_L)
             - settleWL(tg - GATHER_START - GATHER_HOLD, BURST_W, BURST_L);
    float gC = clamp(g, 0.0, 1.0);
    float tb     = tg - (GATHER_START + GATHER_HOLD);
    float charge = smoothstep(-CHARGE_T, 0.0, min(tb, 0.0)) * gC;
    float flash  = tb > 0.0 ? exp(-tb * FLASH_DECAY) : 0.0;
    float gBright = mix(1.0, GATHER_DIM, gC) * (1.0 + CHARGE_GLOW*charge + FLASH_GAIN*flash);
    vec3  total3 = vec3(1e5);
    vec3  cAcc   = vec3(0.0);
    float wAcc   = 1e-6;
    for(int i=0; i<N; i++){
        float fi   = float(i);
        float seed = hash11(fi);
        float ang = fi/float(N)*TAU + t*0.35;
        vec2 dir  = vec2(cos(ang), sin(ang));
        float R = 0.17 + 0.010*sin(t*1.0) + 0.007*sin(t*1.3 + seed*TAU);
        float pairId   = mod(fi, 3.0);
        float moverLow = mod(k + pairId, 2.0);
        float isMover  = (fi < 2.5) ? step(moverLow, 0.5) : step(0.5, moverLow);
        float goStart  = pairId * STAGGER;
        float retStart = 3.0*STAGGER + HOLD + pairId * STAGGER;
        float m   = (settle(te - goStart)           - settle(te - retStart))           * isMover;
        float rec = (settle(te - goStart - REC_LAG) - settle(te - retStart - REC_LAG)) * (1.0 - isMover);
        float rSelf = dotR(fi, seed, t);
        rSelf = mix(rSelf, 0.036, gC);
        rSelf *= 1.0 - CHARGE_SHRK * charge;
        float fj    = mod(fi + 3.0, 6.0);
        float rPart = dotR(fj, hash11(fj), t);
        float deep   = -(R + RECOIL) - PIERCE * rPart;
        float radial = mix(R, deep, m) + RECOIL * rec;
        radial = mix(radial, GATHER_R, g);
        vec2  pos    = radial * dir;
        float sdR = dotSD(p - SPECTRAL.r*dir, pos, rSelf, t, fi, 1.0 - gC);
        float sdG = dotSD(p - SPECTRAL.g*dir, pos, rSelf, t, fi, 1.0 - gC);
        float sdB = dotSD(p - SPECTRAL.b*dir, pos, rSelf, t, fi, 1.0 - gC);
        total3 = vec3( smin(total3.r, sdR, SMOOTH_K),
                       smin(total3.g, sdG, SMOOTH_K),
                       smin(total3.b, sdB, SMOOTH_K) );
        float hue = fract(fi/float(N) + t*HUE_SPEED) * HUE_SPAN;
        vec3 dotCol = mix(vec3(1.0), hue2rgb(hue), SAT);
        float w = exp(-sdG * COLOR_K);
        cAcc += w * dotCol;
        wAcc += w;
    }
    vec3 sd3    = max(total3, vec3(0.0)) + 1e-4;
    vec3 core3  = clamp(INTENSITY / pow(sd3, vec3(FALLOFF_P)), 0.0, 1.0);
    vec3 edge3  = 1.0 - smoothstep(vec3(FADE_START), vec3(FADE_END), sd3);
    vec3 bright = core3 * edge3 * gBright;
    return bright * (cAcc / wAcc);
}
void mainImage(out vec4 fragColor, in vec2 fragCoord){
    vec2 res = iResolution.xy;
    vec2 p = (2.0*fragCoord - res) / min(res.x, res.y);
    float t = iTime;
    p /= 1.0 + 0.03*sin(t*1.0);
    vec3 col = scene(p, t);
    col *= 1.0 + 0.05*sin(t*1.0 + 1.0);
    col = pow(col, vec3(1.0/1.2));
    col = min(col, 1.0);
    float n = fract(sin(dot(fragCoord, vec2(12.9898,78.233)))*43758.5453);
    col += (n - 0.5)/255.0;
    fragColor = vec4(col, 1.0);
}
void main(){ mainImage(gl_FragColor, gl_FragCoord.xy); }`

const FRAGMENT_SHADERS: Record<SiriWaveVariant, string> = {
  wave: WAVE_SHADER,
  "fluid-dots": FLUID_DOTS_SHADER,
}

export interface SiriWaveProps
  extends Omit<React.HTMLAttributes<HTMLCanvasElement>, "children"> {
  /** Which shader to render. */
  variant?: SiriWaveVariant
  /** CSS display size of the square canvas, in px. */
  size?: number
  /** Internal render resolution multiplier (lower = cheaper/blurrier). */
  renderScale?: number
}

export function SiriWave({
  variant = "wave",
  size = 420,
  renderScale = 0.75,
  className,
  style,
  ...props
}: SiriWaveProps) {
  const canvasRef = React.useRef<HTMLCanvasElement>(null)

  React.useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const gl = canvas.getContext("webgl")
    if (!gl) return

    const compile = (type: number, src: string) => {
      const shader = gl.createShader(type)!
      gl.shaderSource(shader, src)
      gl.compileShader(shader)
      if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        const log = gl.getShaderInfoLog(shader)
        gl.deleteShader(shader)
        throw new Error(log ?? "shader compile error")
      }
      return shader
    }

    const program = gl.createProgram()!
    const vs = compile(gl.VERTEX_SHADER, VERTEX_SHADER)
    const fs = compile(gl.FRAGMENT_SHADER, FRAGMENT_SHADERS[variant])
    gl.attachShader(program, vs)
    gl.attachShader(program, fs)
    gl.linkProgram(program)
    gl.useProgram(program)

    const buffer = gl.createBuffer()
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer)
    gl.bufferData(
      gl.ARRAY_BUFFER,
      new Float32Array([-1, -1, 3, -1, -1, 3]),
      gl.STATIC_DRAW,
    )
    const aPos = gl.getAttribLocation(program, "aPos")
    gl.enableVertexAttribArray(aPos)
    gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0)

    const uResolution = gl.getUniformLocation(program, "iResolution")
    const uTime = gl.getUniformLocation(program, "iTime")

    const dim = Math.round(size * renderScale)
    canvas.width = dim
    canvas.height = dim
    gl.viewport(0, 0, dim, dim)

    const start =
      typeof performance !== "undefined" ? performance.now() : Date.now()
    let raf = 0
    const frame = () => {
      const now =
        typeof performance !== "undefined" ? performance.now() : Date.now()
      const t = (now - start) / 1000
      gl.uniform2f(uResolution, dim, dim)
      gl.uniform1f(uTime, t)
      gl.drawArrays(gl.TRIANGLES, 0, 3)
      raf = requestAnimationFrame(frame)
    }
    frame()

    return () => {
      cancelAnimationFrame(raf)
      gl.deleteProgram(program)
      gl.deleteShader(vs)
      gl.deleteShader(fs)
      gl.deleteBuffer(buffer)
    }
  }, [variant, size, renderScale])

  return (
    <canvas
      ref={canvasRef}
      className={cn("block rounded-[20px] bg-black", className)}
      style={{ width: size, height: size, ...style }}
      {...props}
    />
  )
}

export default SiriWave


demo.tsx
import { SiriWave } from "@/components/ui/siri-wave"

export default function SiriWaveDemo() {
  return (
    <div className="flex min-h-screen w-full items-center justify-center bg-[#0a0a0c] p-8">
      <SiriWave
        variant="wave"
        size={360}
        className="shadow-[0_20px_60px_rgba(0,0,0,0.6)]"
      />
    </div>
  )
}

```

Implementation Guidelines
 1. Analyze the component structure and identify all required dependencies
 2. Review the component's argumens and state
 3. Identify any required context providers or hooks and install them
 4. Questions to Ask
 - What data/props will be passed to this component?
 - Are there any specific state management requirements?
 - Are there any required assets (images, icons, etc.)?
 - What is the expected responsive behavior?
 - What is the best place to use this component in the app?

Steps to integrate
 0. Copy paste all the code above in the correct directories
 1. Install external dependencies
 2. Fill image assets with Unsplash stock images you know exist
 3. Use lucide-react icons for svgs or logos if component requires them

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

You are given a task to integrate an existing React component in the codebase

The codebase should support:
- shadcn project structure  
- Tailwind CSS
- Typescript

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind or Typescript.

Determine the default path for components and styles. 
If default path for components is not /components/ui, provide instructions on why it's important to create this folder
Copy-paste this component to /components/ui folder:
```tsx
progressive-flux-loader.tsx
"use client";

import * as React from "react";
import {
  AnimatePresence,
  motion,
  useReducedMotion,
  type Transition,
} from "framer-motion";

import { cn } from "@/lib/utils";

/* ── types ───────────────────────────────────────────────────── */

export interface ProgressiveFluxPhase {
  /** Progress threshold (`0`–`100`) at or past which `label` is shown. */
  at: number;
  /** Text revealed once this threshold is reached. */
  label: string;
}

export interface ProgressiveFluxLoaderProps {
  /**
   * Controlled progress, `0`–`100`. When set, the loader follows this value and
   * the phase label switches at the configured thresholds. Omit it to let the
   * loader run its own looping sweep.
   */
  value?: number;
  /** Phase thresholds and their labels. Each `at` is a `0`–`100` mark. */
  phases?: ProgressiveFluxPhase[];
  /** Seconds for one full sweep when uncontrolled. Default `12`. */
  duration?: number;
  /** Restart from `0` after reaching `100` (uncontrolled only). Default `true`. */
  loop?: boolean;
  /** Show the animated phase label above the bar. Default `true`. */
  showLabel?: boolean;
  /**
   * CSS background for the bar fill. Defaults to the signature vivid blue → cyan
   * flux gradient. Pass any CSS background to replace it, or recolor the default
   * via the `--flux-from` / `--flux-to` CSS variables (e.g. set them to
   * `hsl(var(--primary))` to follow the theme).
   */
  gradient?: string;
  /** Fires once when progress reaches `100` — in both controlled and uncontrolled modes. */
  onComplete?: () => void;
  /** Classes for the root wrapper. */
  className?: string;
  /** Classes for the bar track. */
  barClassName?: string;
  /** Classes for the phase label. */
  textClassName?: string;
}

/* ── constants ───────────────────────────────────────────────── */

const DEFAULT_PHASES: ProgressiveFluxPhase[] = [
  { at: 0, label: "starting up" },
  { at: 25, label: "loading assets" },
  { at: 55, label: "preparing magic" },
  { at: 80, label: "almost there" },
  { at: 100, label: "all done" },
];

// Signature "flux" palette — a vivid blue → cyan → blue fill. The two end
// colors are read from CSS variables with built-in defaults, so the bar can be
// recolored per instance without touching the component: set `--flux-from` /
// `--flux-to` (e.g. to `hsl(var(--primary))` to follow the theme), or override
// the whole fill with the `gradient` prop. The surrounding track and label stay
// on shadcn theme tokens, so the loader still adapts to light and dark. These
// are component-level custom properties, so the v3 build leaves them untouched
// and the fill renders identically on Tailwind v3 and v4.
const FLUX_FROM = "var(--flux-from, #1d6ffb)";
const FLUX_TO = "var(--flux-to, #74e1ff)";
const FLUX_MID = `color-mix(in oklab, ${FLUX_FROM}, ${FLUX_TO})`;

const DEFAULT_GRADIENT = `linear-gradient(90deg, ${FLUX_FROM} 0%, ${FLUX_MID} 35%, ${FLUX_TO} 55%, ${FLUX_MID} 78%, ${FLUX_FROM} 100%)`;

// Colored glow drawn from the same flux palette, a white top-edge highlight,
// and a deep-blue inset for depth.
const BAR_SHADOW = `0 0 18px color-mix(in oklab, ${FLUX_FROM} 55%, transparent), 0 0 32px color-mix(in oklab, ${FLUX_TO} 40%, transparent), inset 0 1.5px 0 rgba(255, 255, 255, 0.5), inset 0 -2px 3px rgba(0, 40, 120, 0.35)`;

// White sweep over the colored fill (blended with `screen`), so the highlight
// reads as a bright glide regardless of theme.
const SHEEN_GRADIENT =
  "linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.55) 50%, transparent 100%)";

const Z_TRANSITION: Transition = { duration: 0.9, ease: [0.22, 1, 0.36, 1] };
const LETTER_TRANSITION: Transition = {
  duration: 0.45,
  ease: [0.22, 1, 0.36, 1],
};

/* ── helpers ─────────────────────────────────────────────────── */

/** Latest label whose threshold has been crossed. Expects pre-sorted phases. */
function pickLabel(value: number, sortedPhases: ProgressiveFluxPhase[]) {
  let active = sortedPhases[0]?.label ?? "";
  for (const phase of sortedPhases) {
    if (value >= phase.at) active = phase.label;
  }
  return active;
}

/* ── label ───────────────────────────────────────────────────── */

interface FluxLabelProps {
  label: string;
  /** Render plain, static text instead of the 3D fly-in (reduced motion). */
  reduced: boolean;
  className?: string;
}

// The label is decorative and `aria-hidden`; the progressbar carries the spoken
// progress via `aria-valuetext`. Under reduced motion it is plain static text.
function FluxLabel({ label, reduced, className }: FluxLabelProps) {
  const base = cn(
    "absolute inset-0 flex items-center justify-center text-center text-3xl font-semibold tracking-tight text-muted-foreground sm:text-4xl",
    className,
  );

  if (reduced) {
    return (
      <div aria-hidden className={base}>
        {label}
      </div>
    );
  }

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={label}
        aria-hidden
        className={base}
        style={{ transformStyle: "preserve-3d" }}
        initial={{ opacity: 0, z: -380, scale: 0.65, filter: "blur(14px)" }}
        animate={{
          opacity: [0, 1, 1, 1],
          z: [-380, 60, -8, 0],
          scale: [0.65, 1.08, 0.985, 1],
          filter: ["blur(14px)", "blur(0px)", "blur(0px)", "blur(0px)"],
        }}
        exit={{
          opacity: 0,
          z: 220,
          scale: 1.35,
          filter: "blur(10px)",
          transition: { duration: 0.45, ease: [0.7, 0, 0.84, 0] },
        }}
        transition={Z_TRANSITION}
      >
        <span className="inline-flex">
          {label.split("").map((char, index) => (
            <motion.span
              key={`${label}-${index}`}
              className="inline-block"
              initial={{ opacity: 0, y: 12, filter: "blur(8px)" }}
              animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
              transition={{ ...LETTER_TRANSITION, delay: 0.18 + index * 0.035 }}
            >
              {char === " " ? " " : char}
            </motion.span>
          ))}
        </span>
      </motion.div>
    </AnimatePresence>
  );
}

/* ── component ───────────────────────────────────────────────── */

export function ProgressiveFluxLoader({
  value,
  phases = DEFAULT_PHASES,
  duration = 12,
  loop = true,
  showLabel = true,
  gradient = DEFAULT_GRADIENT,
  onComplete,
  className,
  barClassName,
  textClassName,
}: ProgressiveFluxLoaderProps) {
  const reduced = !!useReducedMotion();
  const isControlled = typeof value === "number";
  const [internal, setInternal] = React.useState(0);

  // Keep the latest `onComplete` in a ref so a fresh inline callback on every
  // parent render never tears down and restarts the sweep below.
  const onCompleteRef = React.useRef(onComplete);
  React.useEffect(() => {
    onCompleteRef.current = onComplete;
  });

  const completedRef = React.useRef(false);

  // Uncontrolled self-run sweep.
  React.useEffect(() => {
    if (isControlled) return;
    let raf = 0;
    let timer = 0;
    let start: number | null = null;
    const totalMs = Math.max(500, duration * 1000);

    const tick = (ts: number) => {
      if (start === null) start = ts;
      const pct = Math.min(100, ((ts - start) / totalMs) * 100);
      setInternal(pct);
      if (pct >= 100) {
        if (!completedRef.current) {
          completedRef.current = true;
          onCompleteRef.current?.();
        }
        if (loop) {
          start = null;
          completedRef.current = false;
          timer = window.setTimeout(() => {
            setInternal(0);
            raf = requestAnimationFrame(tick);
          }, 700);
        }
        return;
      }
      raf = requestAnimationFrame(tick);
    };

    raf = requestAnimationFrame(tick);
    return () => {
      cancelAnimationFrame(raf);
      clearTimeout(timer);
    };
  }, [isControlled, duration, loop]);

  const raw = isControlled ? value! : internal;
  const current = Number.isFinite(raw) ? Math.min(100, Math.max(0, raw)) : 0;

  // Controlled completion: fire once when `value` crosses 100, re-arm below it.
  React.useEffect(() => {
    if (!isControlled) return;
    if (current >= 100 && !completedRef.current) {
      completedRef.current = true;
      onCompleteRef.current?.();
    } else if (current < 100) {
      completedRef.current = false;
    }
  }, [isControlled, current]);

  const sortedPhases = React.useMemo(
    () => [...phases].sort((a, b) => a.at - b.at),
    [phases],
  );
  const label = React.useMemo(
    () => pickLabel(current, sortedPhases),
    [current, sortedPhases],
  );
  const rounded = Math.round(current);

  return (
    <div
      className={cn(
        "mx-auto flex w-full max-w-md flex-col items-center gap-8",
        className,
      )}
    >
      {showLabel && (
        <div
          className="relative h-16 w-full select-none"
          style={reduced ? undefined : { perspective: "1000px" }}
        >
          <FluxLabel
            label={label}
            reduced={reduced}
            className={textClassName}
          />
        </div>
      )}

      <div
        className={cn(
          "relative h-5 w-full overflow-hidden rounded-full bg-muted shadow-[inset_0_2px_3px_rgba(0,0,0,0.09),inset_0_-1px_2px_rgba(255,255,255,0.7)] dark:shadow-[inset_0_2px_3px_rgba(0,0,0,0.45),inset_0_-1px_2px_rgba(255,255,255,0.05)]",
          barClassName,
        )}
        role="progressbar"
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={rounded}
        aria-valuetext={label ? `${rounded}% – ${label}` : `${rounded}%`}
        aria-label="Loading"
      >
        <motion.div
          className="relative h-full rounded-full"
          style={{ background: gradient, boxShadow: BAR_SHADOW }}
          initial={false}
          animate={{ width: `${current}%` }}
          transition={
            reduced
              ? { duration: 0 }
              : { duration: 0.55, ease: [0.22, 1, 0.36, 1] }
          }
        >
          {!reduced && (
            <motion.span
              aria-hidden
              className="pointer-events-none absolute inset-y-0 left-0 w-1/2 rounded-full"
              style={{ background: SHEEN_GRADIENT, mixBlendMode: "screen" }}
              animate={{ x: ["-110%", "210%"] }}
              transition={{ duration: 1.6, ease: "linear", repeat: Infinity }}
            />
          )}
        </motion.div>
      </div>
    </div>
  );
}

export default ProgressiveFluxLoader;


demo.tsx
"use client";

import * as React from "react";

import { ProgressiveFluxLoader } from "@/components/ui/progressive-flux-loader";

const PHASES = [
  { at: 0, label: "uploading" },
  { at: 40, label: "processing" },
  { at: 75, label: "finalizing" },
  { at: 100, label: "complete" },
];
 

export default function DemoOne() {
  // Drive the loader from simulated upload progress so the fill, phase labels,
  // and completion are all visible in the preview.
  const [progress, setProgress] = React.useState(0);
 
  React.useEffect(() => {
    const id = setInterval(() => {
      setProgress((p) => (p >= 100 ? 0 : Math.min(100, p + 2)));
    }, 200);
    return () => clearInterval(id);
  }, []);
 
  return (
    <div className="flex min-h-[420px] w-full items-center justify-center px-6 py-16">
      <ProgressiveFluxLoader value={progress} phases={PHASES} />
    </div>
  );
}

```

Install NPM dependencies:
```bash
framer-motion
```

Implementation Guidelines
 1. Analyze the component structure and identify all required dependencies
 2. Review the component's argumens and state
 3. Identify any required context providers or hooks and install them
 4. Questions to Ask
 - What data/props will be passed to this component?
 - Are there any specific state management requirements?
 - Are there any required assets (images, icons, etc.)?
 - What is the expected responsive behavior?
 - What is the best place to use this component in the app?

Steps to integrate
 0. Copy paste all the code above in the correct directories
 1. Install external dependencies
 2. Fill image assets with Unsplash stock images you know exist
 3. Use lucide-react icons for svgs or logos if component requires them


:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

You are given a task to integrate an existing React component in the codebase

The codebase should support:
- shadcn project structure  
- Tailwind CSS
- Typescript

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind or Typescript.

Determine the default path for components and styles. 
If default path for components is not /components/ui, provide instructions on why it's important to create this folder
Copy-paste this component to /components/ui folder:
```tsx
animated-hud-targeting-ui.tsx
"use client";

import type React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils"
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

interface TargetingUIProps {
  className?: string;
  pathColors?: {
    light?: string;
    dark?: string;
  };
}

interface HudFrameProps {
  children?: React.ReactNode
  backgroundImage?: string
  backgroundColor?: string
  backgroundVideo?: string
}

export function TargetingUI({
  className,
  pathColors = { light: "white", dark: "white" }
}: TargetingUIProps) {
  const { theme } = useTheme();
  const [mounted, setMounted] = useState(false);

  // Prevent hydration mismatch by waiting for client-side mount
  useEffect(() => {
    setMounted(true);
  }, []);

  const isDark = mounted ? theme === "dark" : true; // Default to dark mode during SSR
  const pathColor = isDark ? pathColors.dark : pathColors.light;
  return (
    <svg 
      width="237" 
      height="220" 
      viewBox="0 0 237 220" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* TOP TARGETING SYSTEM */}
      {/* TOP ROUNDED PATTERN */}
      <motion.g
        transform="translate(90, 50)"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8, duration: 0.2 }}
      >
        <motion.path d="M28 0.953125H27.75V2.82313H28V0.953125Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.8, duration: 0.1 }}
        />
        <motion.path d="M25.0776 1.03902L24.8281 1.05469L24.9453 2.92101L25.1948 2.90534L25.0776 1.03902Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.82, duration: 0.1 }}
        />
        <motion.path d="M22.1621 1.3046L21.9141 1.33594L22.1485 3.19119L22.3965 3.15985L22.1621 1.3046Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.84, duration: 0.1 }}
        />
        <motion.path d="M19.2778 1.75763L19.0312 1.80469L19.3818 3.64153L19.6284 3.59448L19.2778 1.75763Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.86, duration: 0.1 }}
        />
        <motion.path d="M16.4218 2.38304L16.1797 2.44531L16.6455 4.25637L16.8876 4.19409L16.4218 2.38304Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.88, duration: 0.1 }}
        />
        <motion.path d="M13.9452 5.05031L13.3672 3.27231L13.6052 3.19531L14.1832 4.97331L13.9452 5.05031Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.90, duration: 0.1 }}
        />
        <motion.path d="M10.8575 4.18149L10.625 4.27344L11.3124 6.01144L11.5449 5.9195L10.8575 4.18149Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.92, duration: 0.1 }}
        />
        <motion.path d="M8.16372 5.32327L7.9375 5.42969L8.7335 7.12181L8.95972 7.0154L8.16372 5.32327Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.94, duration: 0.1 }}
        />
        <motion.path d="M5.55504 6.66086L5.33594 6.78125L6.23644 8.42015L6.45555 8.29976L5.55504 6.66086Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.96, duration: 0.1 }}
        />
        <motion.path d="M3.0392 8.13947L2.82812 8.27344L3.8302 9.85228L4.04128 9.71831L3.0392 8.13947Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.98, duration: 0.1 }}
        />
        <motion.path d="M1.51206 11.4324L0.414062 9.91944L0.617058 9.77344L1.71506 11.2864L1.51206 11.4324Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 1.0, duration: 0.1 }}
        />
        <motion.path d="M30.6713 1.03208L30.5547 2.89844L30.8042 2.91403L30.9208 1.04767L30.6713 1.03208Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.82, duration: 0.1 }}
        />
        <motion.path d="M33.5853 1.30873L33.3516 3.16406L33.5996 3.19531L33.8334 1.33998L33.5853 1.30873Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.84, duration: 0.1 }}
        />
        <motion.path d="M36.4749 1.75677L36.125 3.59375L36.3716 3.64071L36.7215 1.80374L36.4749 1.75677Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.86, duration: 0.1 }}
        />
        <motion.path d="M39.1092 4.25681L38.8672 4.19381L39.3312 2.38281L39.5742 2.44581L39.1092 4.25681Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.88, duration: 0.1 }}
        />
        <motion.path d="M41.8005 5.05031L41.5625 4.97331L42.1405 3.19531L42.3785 3.27231L41.8005 5.05031Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.90, duration: 0.1 }}
        />
        <motion.path d="M44.8979 4.16698L44.2109 5.90625L44.4435 5.99809L45.1304 4.25882L44.8979 4.16698Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.92, duration: 0.1 }}
        />
        <motion.path d="M47.5842 5.32312L46.7891 7.01562L47.0153 7.12193L47.8105 5.42942L47.5842 5.32312Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.94, duration: 0.1 }}
        />
        <motion.path d="M50.197 6.65775L49.2969 8.29688L49.516 8.41721L50.4161 6.77808L50.197 6.65775Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.96, duration: 0.1 }}
        />
        <motion.path d="M52.7203 8.13959L51.7188 9.71875L51.9299 9.85265L52.9315 8.27349L52.7203 8.13959Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.98, duration: 0.1 }}
        />
        <motion.path d="M54.2421 11.4324L54.0391 11.2864L55.1371 9.77344L55.3401 9.91944L54.2421 11.4324Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 1.0, duration: 0.1 }}
        />
      </motion.g>

      {/* Left diagonal line - animates from top to bottom */}
      <motion.line 
        x1="0.176777" 
        y1="0.823223" 
        x2="74.1768" 
        y2="74.8232" 
        stroke={pathColor} 
        strokeWidth="0.5"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ 
          duration: 0.8, 
          ease: "easeOut",
          delay: 0.2 
        }}
      />
      
      {/* Middle horizontal line - expands from center outward */}
      <motion.line 
        x1="74" 
        y1="74.75" 
        x2="164" 
        y2="74.75" 
        stroke={pathColor} 
        strokeWidth="0.5"
        initial={{ 
          pathLength: 0,
          pathOffset: 0.5 
        }}
        animate={{ 
          pathLength: 1,
          pathOffset: 0 
        }}
        transition={{ 
          duration: 0.6, 
          ease: "easeOut" 
        }}
      />
      
      {/* Right diagonal line - animates from top to bottom */}
      <motion.line 
        x1="236.822" 
        y1="0.82443" 
        x2="163.822" 
        y2="74.8244" 
        stroke={pathColor} 
        strokeWidth="0.5"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ 
          duration: 0.8, 
          ease: "easeOut",
          delay: 0.2 
        }}
      />
      
      {/* Top system - Left side L-shaped dots */}
      <motion.circle
        cx="78"
        cy="66"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2, duration: 0.3 }}
      />
      <motion.circle
        cx="78"
        cy="70"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.3, duration: 0.3 }}
      />
      <motion.circle
        cx="82"
        cy="70"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.4, duration: 0.3 }}
      />
      
      {/* Top system - Right side L-shaped dots (mirrored) */}
      <motion.circle
        cx="159"
        cy="66"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2, duration: 0.3 }}
      />
      <motion.circle
        cx="155"
        cy="70"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.3, duration: 0.3 }}
      />
      <motion.circle
        cx="159"
        cy="70"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.4, duration: 0.3 }}
      />

      {/* OUTER CIRCLE - centered between targeting systems */}
      <g transform="translate(29, 22)">
        <motion.path 
          d="M89.455 175.334C69.3083 175.288 49.7881 168.326 34.1599 155.612C18.5318 142.898 7.74354 125.203 3.6 105.486L0 101.886V73.5335L3.578 69.9575C7.65877 50.1962 18.4297 32.4468 34.0743 19.7028C49.7188 6.95881 69.2797 0 89.458 0C109.636 0 129.197 6.95881 144.842 19.7028C160.486 32.4468 171.257 50.1962 175.338 69.9575L178.914 73.5335V101.884L175.314 105.484C171.171 125.202 160.383 142.898 144.753 155.613C129.124 168.328 109.603 175.29 89.455 175.334ZM0.747999 101.574L4.289 105.116L4.312 105.225C8.35779 124.817 19.0363 142.414 34.5465 155.048C50.0567 167.683 69.4496 174.582 89.4545 174.582C109.459 174.582 128.852 167.683 144.363 155.048C159.873 142.414 170.551 124.817 174.597 105.225L174.62 105.116L178.161 101.574V73.8445L174.646 70.3275L174.623 70.2165C170.598 50.6003 159.926 32.9746 144.408 20.3176C128.891 7.66049 109.48 0.747999 89.455 0.747999C69.4302 0.747999 50.0192 7.66049 34.5017 20.3176C18.9842 32.9746 8.31157 50.6003 4.287 70.2165L4.264 70.3275L0.747999 73.8445V101.574Z" 
          fill="#ffffff80"
          style={{ transformOrigin: "89.5px 87.5px" }}
          initial={{ rotate: 90 }}
          animate={{ rotate: 0 }}
          transition={{ 
            duration: 1.0, 
            ease: "easeOut"
          }}
        />

        {/* LEFT CHAMBER INSERT */}
        <motion.g
          transform="translate(3, 82)"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.6, duration: 0.4 }}
        >
          <motion.path d="M1.25362 0.601562H0.640625V1.21456H1.25362V0.601562Z" fill={pathColor}/>
          <motion.path d="M1.25362 2.82812H0.640625V2.97112H1.25362V2.82812Z" fill={pathColor}/>
          <motion.path d="M1.25362 3.14844H0.640625V3.29144H1.25362V3.14844Z" fill={pathColor}/>
          <motion.path d="M1.25362 6.67969H0.640625V9.15668H1.25362V6.67969Z" fill={pathColor}/>
          <motion.path d="M1.25362 3.95312H0.640625V4.09612H1.25362V3.95312Z" fill={pathColor}/>
          <motion.path d="M1.25362 4.8125H0.640625V4.9555H1.25362V4.8125Z" fill={pathColor}/>
          <motion.path d="M1.25362 5.09375H0.640625V5.23675H1.25362V5.09375Z" fill={pathColor}/>
          <motion.path d="M1.25362 5.375H0.640625V5.51801H1.25362V5.375Z" fill={pathColor}/>
          <motion.path d="M1.25362 5.65625H0.640625V5.79925H1.25362V5.65625Z" fill={pathColor}/>
          <motion.path d="M1.25362 10.0312H0.640625V10.1742H1.25362V10.0312Z" fill={pathColor}/>
          <motion.path d="M1.25362 10.5312H0.640625V10.6742H1.25362V10.5312Z" fill={pathColor}/>
        </motion.g>

        {/* RIGHT CHAMBER INSERT */}
        <motion.g
          transform="translate(174, 82)"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.6, duration: 0.4 }}
        >
          <motion.path d="M1.25362 0.601562H0.640625V1.21456H1.25362V0.601562Z" fill={pathColor}/>
          <motion.path d="M1.25362 2.82812H0.640625V2.97112H1.25362V2.82812Z" fill={pathColor}/>
          <motion.path d="M1.25362 3.14844H0.640625V3.29144H1.25362V3.14844Z" fill={pathColor}/>
          <motion.path d="M1.25362 6.67969H0.640625V9.15668H1.25362V6.67969Z" fill={pathColor}/>
          <motion.path d="M1.25362 3.95312H0.640625V4.09612H1.25362V3.95312Z" fill={pathColor}/>
          <motion.path d="M1.25362 4.8125H0.640625V4.9555H1.25362V4.8125Z" fill={pathColor}/>
          <motion.path d="M1.25362 5.09375H0.640625V5.23675H1.25362V5.09375Z" fill={pathColor}/>
          <motion.path d="M1.25362 5.375H0.640625V5.51801H1.25362V5.375Z" fill={pathColor}/>
          <motion.path d="M1.25362 5.65625H0.640625V5.79925H1.25362V5.65625Z" fill={pathColor}/>
          <motion.path d="M1.25362 10.0312H0.640625V10.1742H1.25362V10.0312Z" fill={pathColor}/>
          <motion.path d="M1.25362 10.5312H0.640625V10.6742H1.25362V10.5312Z" fill={pathColor}/>
        </motion.g>

        {/* INNER CIRCLES */}
        {/* First inner circle - starts from top (0 degrees) */}
        <motion.circle
          cx="89.5"
          cy="87.5"
          r="80"
          fill="none"
          stroke={pathColor}
          strokeWidth="0.5"
          strokeLinecap="round"
          style={{ transformOrigin: "89.5px 87.5px" }}
          initial={{ 
            pathLength: 0,
            rotate: 0 
          }}
          animate={{ 
            pathLength: 1.1,
            rotate: 0 
          }}
          transition={{ 
            duration: 1.2, 
            ease: "easeOut",
            delay: 0.2
          }}
        />

        {/* Second inner circle - starts from bottom (180 degrees) */}
        <motion.circle
          cx="89.5"
          cy="87.5"
          r="72"
          fill="none"
          stroke={pathColor}
          strokeWidth="0.5"
          strokeLinecap="round"
          style={{ transformOrigin: "89.5px 87.5px" }}
          initial={{ 
            pathLength: 0,
            rotate: 180 
          }}
          animate={{ 
            pathLength: 1.1,
            rotate: 180 
          }}
          transition={{ 
            duration: 1.2, 
            ease: "easeOut",
            delay: 0.2
          }}
        />

        {/* CENTER TARGETING SYSTEM */}
        <g transform="translate(44.5, 70)">
          {/* TOP LEFT CORNER */}
          <motion.path 
            d="M22.5038 34.3712H16.8358L16.7988 34.3342L12.7578 30.2942L12.9358 30.1172L16.9398 34.1212H22.5038V34.3712Z" 
            fill="none"
            stroke={pathColor}
            strokeWidth="0.5"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ 
              duration: 0.6, 
              ease: "easeOut",
              delay: 1.2 
            }}
          />
          
          {/* TOP RIGHT CORNER */}
          <motion.path 
            d="M72.9112 34.3712H67.2422V34.1212H72.8072L76.8102 30.1172L76.9882 30.2942L72.9112 34.3712Z" 
            fill="none"
            stroke={pathColor}
            strokeWidth="0.5"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ 
              duration: 0.6, 
              ease: "easeOut",
              delay: 1.2 
            }}
          />
          
          {/* CENTER TRIANGLE */}
          <motion.path 
            d="M45.9778 21.5266H43.9898L39.7578 14.1966L40.7508 12.4766H49.2148L50.2148 14.1966L45.9778 21.5266ZM44.2778 21.0266H45.6878L49.6308 14.1966L48.9248 12.9766H41.0408L40.3358 14.1966L44.2778 21.0266Z" 
            fill="none"
            stroke={pathColor}
            strokeWidth="0.5"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ 
              duration: 0.8, 
              ease: "easeOut",
              delay: 1.6 
            }}
          />
          
          {/* LEFT SIDE BRACKET */}
          <motion.path 
            d="M1.48806 20.6704L0.414062 19.5954V16.0804L1.50806 14.9844L1.68606 15.1614L0.664062 16.1834V19.4924L1.66606 20.4934L1.48806 20.6704Z" 
            fill="none"
            stroke={pathColor}
            strokeWidth="0.5"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ 
              duration: 0.6, 
              ease: "easeOut",
              delay: 2.0 
            }}
          />
          
          {/* RIGHT SIDE BRACKET */}
          <motion.path 
            d="M88.2663 20.6704L88.0903 20.4934L89.0923 19.4924V16.1834L88.0703 15.1614L88.2463 14.9844L89.3423 16.0804V19.5954L88.2663 20.6704Z" 
            fill="none"
            stroke={pathColor}
            strokeWidth="0.5"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ 
              duration: 0.6, 
              ease: "easeOut",
              delay: 2.0 
            }}
          />
          
          {/* BOTTOM LEFT CORNER */}
          <motion.path 
            d="M12.9358 4.98056L12.7578 4.80356L16.8358 0.726562H22.5038V0.976562H16.9398L12.9358 4.98056Z" 
            fill="none"
            stroke={pathColor}
            strokeWidth="0.5"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ 
              duration: 0.6, 
              ease: "easeOut",
              delay: 2.0 
            }}
          />
          
          {/* BOTTOM RIGHT CORNER */}
          <motion.path 
            d="M76.8102 4.98056L72.8072 0.976562H67.2422V0.726562H72.9112L72.9482 0.763557L76.9882 4.80356L76.8102 4.98056Z" 
            fill="none"
            stroke={pathColor}
            strokeWidth="0.5"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ 
              duration: 0.6, 
              ease: "easeOut",
              delay: 2.0 
            }}
          />
        </g>
      </g>

      {/* LEFT SIDE 2x2 GRID - Outside outer circle */}
      <motion.circle
        cx="15"
        cy="107"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2, duration: 0.3 }}
      />
      <motion.circle
        cx="20"
        cy="107"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.3, duration: 0.3 }}
      />
      <motion.circle
        cx="15"
        cy="112"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.4, duration: 0.3 }}
      />
      <motion.circle
        cx="20"
        cy="112"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5, duration: 0.3 }}
      />

      {/* RIGHT SIDE 2x2 GRID - Outside outer circle */}
      <motion.circle
        cx="217"
        cy="107"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2, duration: 0.3 }}
      />
      <motion.circle
        cx="222"
        cy="107"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.3, duration: 0.3 }}
      />
      <motion.circle
        cx="217"
        cy="112"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.4, duration: 0.3 }}
      />
      <motion.circle
        cx="222"
        cy="112"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5, duration: 0.3 }}
      />

      {/* BOTTOM TARGETING SYSTEM (FLIPPED) */}
      {/* BOTTOM ROUNDED PATTERN (FLIPPED) */}
      <motion.g
        transform="translate(90.5, 173) scale(1, -1)"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8, duration: 0.2 }}
      >
        <motion.path d="M28 0.953125H27.75V2.82313H28V0.953125Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.8, duration: 0.1 }}
        />
        <motion.path d="M25.0776 1.03902L24.8281 1.05469L24.9453 2.92101L25.1948 2.90534L25.0776 1.03902Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.82, duration: 0.1 }}
        />
        <motion.path d="M22.1621 1.3046L21.9141 1.33594L22.1485 3.19119L22.3965 3.15985L22.1621 1.3046Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.84, duration: 0.1 }}
        />
        <motion.path d="M19.2778 1.75763L19.0312 1.80469L19.3818 3.64153L19.6284 3.59448L19.2778 1.75763Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.86, duration: 0.1 }}
        />
        <motion.path d="M16.4218 2.38304L16.1797 2.44531L16.6455 4.25637L16.8876 4.19409L16.4218 2.38304Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.88, duration: 0.1 }}
        />
        <motion.path d="M13.9452 5.05031L13.3672 3.27231L13.6052 3.19531L14.1832 4.97331L13.9452 5.05031Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.90, duration: 0.1 }}
        />
        <motion.path d="M10.8575 4.18149L10.625 4.27344L11.3124 6.01144L11.5449 5.9195L10.8575 4.18149Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.92, duration: 0.1 }}
        />
        <motion.path d="M8.16372 5.32327L7.9375 5.42969L8.7335 7.12181L8.95972 7.0154L8.16372 5.32327Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.94, duration: 0.1 }}
        />
        <motion.path d="M5.55504 6.66086L5.33594 6.78125L6.23644 8.42015L6.45555 8.29976L5.55504 6.66086Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.96, duration: 0.1 }}
        />
        <motion.path d="M3.0392 8.13947L2.82812 8.27344L3.8302 9.85228L4.04128 9.71831L3.0392 8.13947Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.98, duration: 0.1 }}
        />
        <motion.path d="M1.51206 11.4324L0.414062 9.91944L0.617058 9.77344L1.71506 11.2864L1.51206 11.4324Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 1.0, duration: 0.1 }}
        />
        <motion.path d="M30.6713 1.03208L30.5547 2.89844L30.8042 2.91403L30.9208 1.04767L30.6713 1.03208Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.82, duration: 0.1 }}
        />
        <motion.path d="M33.5853 1.30873L33.3516 3.16406L33.5996 3.19531L33.8334 1.33998L33.5853 1.30873Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.84, duration: 0.1 }}
        />
        <motion.path d="M36.4749 1.75677L36.125 3.59375L36.3716 3.64071L36.7215 1.80374L36.4749 1.75677Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.86, duration: 0.1 }}
        />
        <motion.path d="M39.1092 4.25681L38.8672 4.19381L39.3312 2.38281L39.5742 2.44581L39.1092 4.25681Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.88, duration: 0.1 }}
        />
        <motion.path d="M41.8005 5.05031L41.5625 4.97331L42.1405 3.19531L42.3785 3.27231L41.8005 5.05031Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.90, duration: 0.1 }}
        />
        <motion.path d="M44.8979 4.16698L44.2109 5.90625L44.4435 5.99809L45.1304 4.25882L44.8979 4.16698Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.92, duration: 0.1 }}
        />
        <motion.path d="M47.5842 5.32312L46.7891 7.01562L47.0153 7.12193L47.8105 5.42942L47.5842 5.32312Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.94, duration: 0.1 }}
        />
        <motion.path d="M50.197 6.65775L49.2969 8.29688L49.516 8.41721L50.4161 6.77808L50.197 6.65775Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.96, duration: 0.1 }}
        />
        <motion.path d="M52.7203 8.13959L51.7188 9.71875L51.9299 9.85265L52.9315 8.27349L52.7203 8.13959Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 0.98, duration: 0.1 }}
        />
        <motion.path d="M54.2421 11.4324L54.0391 11.2864L55.1371 9.77344L55.3401 9.91944L54.2421 11.4324Z" fill={pathColor} opacity="0.3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ delay: 1.0, duration: 0.1 }}
        />
      </motion.g>
      {/* Left diagonal line - animates from bottom to top (flipped) */}
      <motion.line 
        x1="0.176777" 
        y1="219.176777" 
        x2="74.1768" 
        y2="145.1768" 
        stroke={pathColor} 
        strokeWidth="0.5"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ 
          duration: 0.8, 
          ease: "easeOut",
          delay: 0.2 
        }}
      />
      
      {/* Middle horizontal line - expands from center outward (flipped) */}
      <motion.line 
        x1="74" 
        y1="145.25" 
        x2="164" 
        y2="145.25" 
        stroke={pathColor} 
        strokeWidth="0.5"
        initial={{ 
          pathLength: 0,
          pathOffset: 0.5 
        }}
        animate={{ 
          pathLength: 1,
          pathOffset: 0 
        }}
        transition={{ 
          duration: 0.6, 
          ease: "easeOut" 
        }}
      />
      
      {/* Right diagonal line - animates from bottom to top (flipped) */}
      <motion.line 
        x1="236.822" 
        y1="219.17557" 
        x2="163.822" 
        y2="145.1756" 
        stroke={pathColor} 
        strokeWidth="0.5"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ 
          duration: 0.8, 
          ease: "easeOut",
          delay: 0.2 
        }}
      />
      
      {/* Bottom system - Left side L-shaped dots (flipped) */}
      <motion.circle
        cx="78"
        cy="154"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2, duration: 0.3 }}
      />
      <motion.circle
        cx="78"
        cy="150"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.3, duration: 0.3 }}
      />
      <motion.circle
        cx="82"
        cy="150"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.4, duration: 0.3 }}
      />
      
      {/* Bottom system - Right side L-shaped dots (flipped) */}
      <motion.circle
        cx="159"
        cy="154"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2, duration: 0.3 }}
      />
      <motion.circle
        cx="155"
        cy="150"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.3, duration: 0.3 }}
      />
      <motion.circle
        cx="159"
        cy="150"
        r=".75"
        fill={pathColor}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.4, duration: 0.3 }}
      />
    </svg>
  );
}

export function HudFrame({ children, backgroundImage, backgroundColor, backgroundVideo }: HudFrameProps) {
  return (
    <div className="relative w-full h-full">
      {/* Content area - this is where children will render */}
      <div className="w-full h-full relative z-20">{children}</div>

      {/* HUD Frame Overlay */}
      <div
        className="fixed top-0 left-0 w-screen h-screen pointer-events-none z-10"
        style={
          {
            "--frame-thickness": "8px",
            "--corner-chamfer": "16px",
            "--notch-width": "240px",
            "--notch-depth": "16px",
            "--notch-chamfer": "12px",
            "--frame-padding": "8px",
            "--edge-radius": "50px",
            "--border-width": "0px",
          } as React.CSSProperties
        }
      >
        {/* White border layer (behind) */}
        <div
          className="w-full h-full bg-white"
          style={{
            clipPath: `polygon(
        calc(var(--frame-padding) - var(--border-width)) calc(var(--corner-chamfer) + var(--frame-padding) - var(--border-width)),
        calc(var(--corner-chamfer) + var(--frame-padding) - var(--border-width)) calc(var(--frame-padding) - var(--border-width)),
        calc(50% - var(--notch-width)/2) calc(var(--frame-padding) - var(--border-width)),
        calc(50% - var(--notch-width)/2 + var(--notch-chamfer)) calc(var(--notch-depth) + var(--frame-padding) - var(--border-width)),
        calc(50% + var(--notch-width)/2 - var(--notch-chamfer)) calc(var(--notch-depth) + var(--frame-padding) - var(--border-width)),
        calc(50% + var(--notch-width)/2) calc(var(--frame-padding) - var(--border-width)),
        calc(100% - var(--corner-chamfer) - var(--frame-padding) + var(--border-width)) calc(var(--frame-padding) - var(--border-width)),
        calc(100% - var(--frame-padding) + var(--border-width)) calc(var(--corner-chamfer) + var(--frame-padding) - var(--border-width)),
        calc(100% - var(--frame-padding) + var(--border-width)) calc(50% - var(--notch-width)/2),
        calc(100% - var(--notch-depth) - var(--frame-padding) + var(--border-width)) calc(50% - var(--notch-width)/2 + var(--notch-chamfer)),
        calc(100% - var(--notch-depth) - var(--frame-padding) + var(--border-width)) calc(50% + var(--notch-width)/2 - var(--notch-chamfer)),
        calc(100% - var(--frame-padding) + var(--border-width)) calc(50% + var(--notch-width)/2),
        calc(100% - var(--frame-padding) + var(--border-width)) calc(100% - var(--corner-chamfer) - var(--frame-padding) + var(--border-width)),
        calc(100% - var(--corner-chamfer) - var(--frame-padding) + var(--border-width)) calc(100% - var(--frame-padding) + var(--border-width)),
        calc(50% + var(--notch-width)/2) calc(100% - var(--frame-padding) + var(--border-width)),
        calc(50% + var(--notch-width)/2 - var(--notch-chamfer)) calc(100% - var(--notch-depth) - var(--frame-padding) + var(--border-width)),
        calc(50% - var(--notch-width)/2 + var(--notch-chamfer)) calc(100% - var(--notch-depth) - var(--frame-padding) + var(--border-width)),
        calc(50% - var(--notch-width)/2) calc(100% - var(--frame-padding) + var(--border-width)),
        calc(var(--corner-chamfer) + var(--frame-padding) - var(--border-width)) calc(100% - var(--frame-padding) + var(--border-width)),
        calc(var(--frame-padding) - var(--border-width)) calc(100% - var(--corner-chamfer) - var(--frame-padding) + var(--border-width)),
        calc(var(--frame-padding) - var(--border-width)) calc(50% + var(--notch-width)/2),
        calc(var(--notch-depth) + var(--frame-padding) - var(--border-width)) calc(50% + var(--notch-width)/2 - var(--notch-chamfer)),
        calc(var(--notch-depth) + var(--frame-padding) - var(--border-width)) calc(50% - var(--notch-width)/2 + var(--notch-chamfer)),
        calc(var(--frame-padding) - var(--border-width)) calc(50% - var(--notch-width)/2)
      )`,
            borderRadius: "var(--edge-radius)",
          }}
        />

        {/* Main frame layer with background image */}
        <div
          className={cn("absolute inset-0 w-full h-full bg-cover bg-center bg-no-repeat", backgroundColor ? `bg-[${backgroundColor}]` : "bg-zinc-600 dark:bg-zinc-800")}
          style={{
            backgroundImage: backgroundImage ? `url(${backgroundImage})` : undefined,
            clipPath: `polygon(
        var(--frame-padding) calc(var(--corner-chamfer) + var(--frame-padding)),
        calc(var(--corner-chamfer) + var(--frame-padding)) var(--frame-padding),
        calc(50% - var(--notch-width)/2) var(--frame-padding),
        calc(50% - var(--notch-width)/2 + var(--notch-chamfer)) calc(var(--notch-depth) + var(--frame-padding)),
        calc(50% + var(--notch-width)/2 - var(--notch-chamfer)) calc(var(--notch-depth) + var(--frame-padding)),
        calc(50% + var(--notch-width)/2) var(--frame-padding),
        calc(100% - var(--corner-chamfer) - var(--frame-padding)) var(--frame-padding),
        calc(100% - var(--frame-padding)) calc(var(--corner-chamfer) + var(--frame-padding)),
        calc(100% - var(--frame-padding)) calc(50% - var(--notch-width)/2),
        calc(100% - var(--notch-depth) - var(--frame-padding)) calc(50% - var(--notch-width)/2 + var(--notch-chamfer)),
        calc(100% - var(--notch-depth) - var(--frame-padding)) calc(50% + var(--notch-width)/2 - var(--notch-chamfer)),
        calc(100% - var(--frame-padding)) calc(50% + var(--notch-width)/2),
        calc(100% - var(--frame-padding)) calc(100% - var(--corner-chamfer) - var(--frame-padding)),
        calc(100% - var(--corner-chamfer) - var(--frame-padding)) calc(100% - var(--frame-padding)),
        calc(50% + var(--notch-width)/2) calc(100% - var(--frame-padding)),
        calc(50% + var(--notch-width)/2 - var(--notch-chamfer)) calc(100% - var(--notch-depth) - var(--frame-padding)),
        calc(50% - var(--notch-width)/2 + var(--notch-chamfer)) calc(100% - var(--notch-depth) - var(--frame-padding)),
        calc(50% - var(--notch-width)/2) calc(100% - var(--frame-padding)),
        calc(var(--corner-chamfer) + var(--frame-padding)) calc(100% - var(--frame-padding)),
        var(--frame-padding) calc(100% - var(--corner-chamfer) - var(--frame-padding)),
        var(--frame-padding) calc(50% + var(--notch-width)/2),
        calc(var(--notch-depth) + var(--frame-padding)) calc(50% + var(--notch-width)/2 - var(--notch-chamfer)),
        calc(var(--notch-depth) + var(--frame-padding)) calc(50% - var(--notch-width)/2 + var(--notch-chamfer)),
        var(--frame-padding) calc(50% - var(--notch-width)/2)
      )`,
            borderRadius: "var(--edge-radius)",
          }}
        >
          {/* Background Video */}
          {backgroundVideo && (
            <video
              className="absolute inset-0 w-full h-full object-cover"
              src={backgroundVideo}
              autoPlay
              loop
              muted
              playsInline
              style={{
                clipPath: `polygon(
            var(--frame-padding) calc(var(--corner-chamfer) + var(--frame-padding)),
            calc(var(--corner-chamfer) + var(--frame-padding)) var(--frame-padding),
            calc(50% - var(--notch-width)/2) var(--frame-padding),
            calc(50% - var(--notch-width)/2 + var(--notch-chamfer)) calc(var(--notch-depth) + var(--frame-padding)),
            calc(50% + var(--notch-width)/2 - var(--notch-chamfer)) calc(var(--notch-depth) + var(--frame-padding)),
            calc(50% + var(--notch-width)/2) var(--frame-padding),
            calc(100% - var(--corner-chamfer) - var(--frame-padding)) var(--frame-padding),
            calc(100% - var(--frame-padding)) calc(var(--corner-chamfer) + var(--frame-padding)),
            calc(100% - var(--frame-padding)) calc(50% - var(--notch-width)/2),
            calc(100% - var(--notch-depth) - var(--frame-padding)) calc(50% - var(--notch-width)/2 + var(--notch-chamfer)),
            calc(100% - var(--notch-depth) - var(--frame-padding)) calc(50% + var(--notch-width)/2 - var(--notch-chamfer)),
            calc(100% - var(--frame-padding)) calc(50% + var(--notch-width)/2),
            calc(100% - var(--frame-padding)) calc(100% - var(--corner-chamfer) - var(--frame-padding)),
            calc(100% - var(--corner-chamfer) - var(--frame-padding)) calc(100% - var(--frame-padding)),
            calc(50% + var(--notch-width)/2) calc(100% - var(--frame-padding)),
            calc(50% + var(--notch-width)/2 - var(--notch-chamfer)) calc(100% - var(--notch-depth) - var(--frame-padding)),
            calc(50% - var(--notch-width)/2 + var(--notch-chamfer)) calc(100% - var(--notch-depth) - var(--frame-padding)),
            calc(50% - var(--notch-width)/2) calc(100% - var(--frame-padding)),
            calc(var(--corner-chamfer) + var(--frame-padding)) calc(100% - var(--frame-padding)),
            var(--frame-padding) calc(100% - var(--corner-chamfer) - var(--frame-padding)),
            var(--frame-padding) calc(50% + var(--notch-width)/2),
            calc(var(--notch-depth) + var(--frame-padding)) calc(50% + var(--notch-width)/2 - var(--notch-chamfer)),
            calc(var(--notch-depth) + var(--frame-padding)) calc(50% - var(--notch-width)/2 + var(--notch-chamfer)),
            var(--frame-padding) calc(50% - var(--notch-width)/2)
          )`
              }}
            />
          )}

          {/* Inner transparent cutout */}
          <div
            className="w-full h-full bg-transparent"
            style={{
              clipPath: `polygon(
          calc(var(--frame-thickness) + var(--frame-padding)) calc(var(--corner-chamfer) + var(--frame-thickness) + var(--frame-padding)),
          calc(var(--corner-chamfer) + var(--frame-thickness) + var(--frame-padding)) calc(var(--frame-thickness) + var(--frame-padding)),
          calc(50% - var(--notch-width)/2) calc(var(--frame-thickness) + var(--frame-padding)),
          calc(50% - var(--notch-width)/2 + var(--notch-chamfer)) calc(var(--notch-depth) + var(--frame-thickness) + var(--frame-padding)),
          calc(50% + var(--notch-width)/2 - var(--notch-chamfer)) calc(var(--notch-depth) + var(--frame-thickness) + var(--frame-padding)),
          calc(50% + var(--notch-width)/2) calc(var(--frame-thickness) + var(--frame-padding)),
          calc(100% - var(--corner-chamfer) - var(--frame-thickness) - var(--frame-padding)) calc(var(--frame-thickness) + var(--frame-padding)),
          calc(100% - var(--frame-thickness) - var(--frame-padding)) calc(var(--corner-chamfer) + var(--frame-thickness) + var(--frame-padding)),
          calc(100% - var(--frame-thickness) - var(--frame-padding)) calc(50% - var(--notch-width)/2),
          calc(100% - var(--notch-depth) - var(--frame-thickness) - var(--frame-padding)) calc(50% - var(--notch-width)/2 + var(--notch-chamfer)),
          calc(100% - var(--notch-depth) - var(--frame-thickness) - var(--frame-padding)) calc(50% + var(--notch-width)/2 - var(--notch-chamfer)),
          calc(100% - var(--frame-thickness) - var(--frame-padding)) calc(50% + var(--notch-width)/2),
          calc(100% - var(--frame-thickness) - var(--frame-padding)) calc(100% - var(--corner-chamfer) - var(--frame-thickness) - var(--frame-padding)),
          calc(100% - var(--corner-chamfer) - var(--frame-thickness) - var(--frame-padding)) calc(100% - var(--frame-thickness) - var(--frame-padding)),
          calc(50% + var(--notch-width)/2) calc(100% - var(--frame-thickness) - var(--frame-padding)),
          calc(50% + var(--notch-width)/2 - var(--notch-chamfer)) calc(100% - var(--notch-depth) - var(--frame-thickness) - var(--frame-padding)),
          calc(50% - var(--notch-width)/2 + var(--notch-chamfer)) calc(100% - var(--notch-depth) - var(--frame-thickness) - var(--frame-padding)),
          calc(50% - var(--notch-width)/2) calc(100% - var(--frame-thickness) - var(--frame-padding)),
          calc(var(--corner-chamfer) + var(--frame-thickness) + var(--frame-padding)) calc(100% - var(--frame-thickness) - var(--frame-padding)),
          calc(var(--frame-thickness) + var(--frame-padding)) calc(100% - var(--corner-chamfer) - var(--frame-thickness) - var(--frame-padding)),
          calc(var(--frame-thickness) + var(--frame-padding)) calc(50% + var(--notch-width)/2),
          calc(var(--notch-depth) + var(--frame-thickness) + var(--frame-padding)) calc(50% + var(--notch-width)/2 - var(--notch-chamfer)),
          calc(var(--notch-depth) + var(--frame-thickness) + var(--frame-padding)) calc(50% - var(--notch-width)/2 + var(--notch-chamfer)),
          calc(var(--frame-thickness) + var(--frame-padding)) calc(50% - var(--notch-width)/2)
        )`,
              borderRadius: "calc(var(--edge-radius) - 2px)",
            }}
          />
        </div>
      </div>
    </div>
  )
}


demo.tsx
"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { HudFrame, TargetingUI } from "@/components/ui/animated-hud-targeting-ui";

export default function Page() {
  const [mounted, setMounted] = useState(false);
  const [showTargeting, setShowTargeting] = useState(true);
  const [targetingKey, setTargetingKey] = useState(0);

  useEffect(() => {
    setMounted(true);
  }, []);

  const svgAnimation = {
    hidden: { opacity: 0, scale: 0.95 },
    show: {
      opacity: 1,
      scale: 1,
      transition: {
        duration: 0.8,
        ease: [0.22, 1, 0.36, 1],
      },
    },
    hide: {
      opacity: 0,
      scale: 0.95,
      transition: {
        duration: 0.5,
        ease: [0.22, 1, 0.36, 1],
      },
    },
  };

  return (
    <div className="min-h-screen overflow-hidden">
      <HudFrame>
        <div className="flex flex-col w-full h-screen relative overflow-hidden">
            <TargetingUI className="w-128 h-full" />
        </div>
      </HudFrame>
    </div>
  );
}

```

Install NPM dependencies:
```bash
next-themes, framer-motion
```

Implementation Guidelines
 1. Analyze the component structure and identify all required dependencies
 2. Review the component's argumens and state
 3. Identify any required context providers or hooks and install them
 4. Questions to Ask
 - What data/props will be passed to this component?
 - Are there any specific state management requirements?
 - Are there any required assets (images, icons, etc.)?
 - What is the expected responsive behavior?
 - What is the best place to use this component in the app?

Steps to integrate
 0. Copy paste all the code above in the correct directories
 1. Install external dependencies
 2. Fill image assets with Unsplash stock images you know exist
 3. Use lucide-react icons for svgs or logos if component requires them

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

You are given a task to integrate an existing React component in the codebase

The codebase should support:
- shadcn project structure  
- Tailwind CSS
- Typescript

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind or Typescript.

Determine the default path for components and styles. 
If default path for components is not /components/ui, provide instructions on why it's important to create this folder
Copy-paste this component to /components/ui folder:
```tsx
agent-plan.tsx
"use client";

import React, { useState } from "react";
import {
  CheckCircle2,
  Circle,
  CircleAlert,
  CircleDotDashed,
  CircleX,
} from "lucide-react";
import { motion, AnimatePresence, LayoutGroup } from "framer-motion";

// Type definitions
interface Subtask {
  id: string;
  title: string;
  description: string;
  status: string;
  priority: string;
  tools?: string[]; // Optional array of MCP server tools
}

interface Task {
  id: string;
  title: string;
  description: string;
  status: string;
  priority: string;
  level: number;
  dependencies: string[];
  subtasks: Subtask[];
}

// Initial task data
const initialTasks: Task[] = [
  {
    id: "1",
    title: "Research Project Requirements",
    description:
      "Gather all necessary information about project scope and requirements",
    status: "in-progress",
    priority: "high",
    level: 0,
    dependencies: [],
    subtasks: [
      {
        id: "1.1",
        title: "Interview stakeholders",
        description:
          "Conduct interviews with key stakeholders to understand needs",
        status: "completed",
        priority: "high",
        tools: ["communication-agent", "meeting-scheduler"],
      },
      {
        id: "1.2",
        title: "Review existing documentation",
        description:
          "Go through all available documentation and extract requirements",
        status: "in-progress",
        priority: "medium",
        tools: ["file-system", "browser"],
      },
      {
        id: "1.3",
        title: "Compile findings report",
        description:
          "Create a comprehensive report of all gathered information",
        status: "need-help",
        priority: "medium",
        tools: ["file-system", "markdown-processor"],
      },
    ],
  },
  {
    id: "2",
    title: "Design System Architecture",
    description: "Create the overall system architecture based on requirements",
    status: "in-progress",
    priority: "high",
    level: 0,
    dependencies: [],
    subtasks: [
      {
        id: "2.1",
        title: "Define component structure",
        description: "Map out all required components and their interactions",
        status: "pending",
        priority: "high",
        tools: ["architecture-planner", "diagramming-tool"],
      },
      {
        id: "2.2",
        title: "Create data flow diagrams",
        description:
          "Design diagrams showing how data will flow through the system",
        status: "pending",
        priority: "medium",
        tools: ["diagramming-tool", "file-system"],
      },
      {
        id: "2.3",
        title: "Document API specifications",
        description: "Write detailed specifications for all APIs in the system",
        status: "pending",
        priority: "high",
        tools: ["api-designer", "openapi-generator"],
      },
    ],
  },
  {
    id: "3",
    title: "Implementation Planning",
    description: "Create a detailed plan for implementing the system",
    status: "pending",
    priority: "medium",
    level: 1,
    dependencies: ["1", "2"],
    subtasks: [
      {
        id: "3.1",
        title: "Resource allocation",
        description: "Determine required resources and allocate them to tasks",
        status: "pending",
        priority: "medium",
        tools: ["project-manager", "resource-calculator"],
      },
      {
        id: "3.2",
        title: "Timeline development",
        description: "Create a timeline with milestones and deadlines",
        status: "pending",
        priority: "high",
        tools: ["timeline-generator", "gantt-chart-creator"],
      },
      {
        id: "3.3",
        title: "Risk assessment",
        description:
          "Identify potential risks and develop mitigation strategies",
        status: "pending",
        priority: "medium",
        tools: ["risk-analyzer"],
      },
    ],
  },
  {
    id: "4",
    title: "Development Environment Setup",
    description: "Set up all necessary tools and environments for development",
    status: "in-progress",
    priority: "high",
    level: 0,
    dependencies: [],
    subtasks: [
      {
        id: "4.1",
        title: "Install development tools",
        description:
          "Set up IDEs, version control, and other necessary development tools",
        status: "pending",
        priority: "high",
        tools: ["shell", "package-manager"],
      },
      {
        id: "4.2",
        title: "Configure CI/CD pipeline",
        description: "Set up continuous integration and deployment pipelines",
        status: "pending",
        priority: "medium",
        tools: ["github-actions", "gitlab-ci", "jenkins-connector"],
      },
      {
        id: "4.3",
        title: "Set up testing framework",
        description: "Configure automated testing frameworks for the project",
        status: "pending",
        priority: "high",
        tools: ["test-runner", "shell"],
      },
    ],
  },
  {
    id: "5",
    title: "Initial Development Sprint",
    description: "Execute the first development sprint based on the plan",
    status: "pending",
    priority: "medium",
    level: 1,
    dependencies: ["4"],
    subtasks: [
      {
        id: "5.1",
        title: "Implement core features",
        description:
          "Develop the essential features identified in the requirements",
        status: "pending",
        priority: "high",
        tools: ["code-assistant", "github", "file-system", "shell"],
      },
      {
        id: "5.2",
        title: "Perform unit testing",
        description: "Create and execute unit tests for implemented features",
        status: "pending",
        priority: "medium",
        tools: ["test-runner", "code-coverage-analyzer"],
      },
      {
        id: "5.3",
        title: "Document code",
        description: "Create documentation for the implemented code",
        status: "pending",
        priority: "low",
        tools: ["documentation-generator", "markdown-processor"],
      },
    ],
  },
];

export default function Plan() {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const [expandedTasks, setExpandedTasks] = useState<string[]>(["1"]);
  const [expandedSubtasks, setExpandedSubtasks] = useState<{
    [key: string]: boolean;
  }>({});
  // Add support for reduced motion preference
  const prefersReducedMotion = 
    typeof window !== 'undefined' 
      ? window.matchMedia('(prefers-reduced-motion: reduce)').matches 
      : false;

  // Toggle task expansion
  const toggleTaskExpansion = (taskId: string) => {
    setExpandedTasks((prev) =>
      prev.includes(taskId)
        ? prev.filter((id) => id !== taskId)
        : [...prev, taskId],
    );
  };

  // Toggle subtask expansion
  const toggleSubtaskExpansion = (taskId: string, subtaskId: string) => {
    const key = `${taskId}-${subtaskId}`;
    setExpandedSubtasks((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  // Toggle task status
  const toggleTaskStatus = (taskId: string) => {
    setTasks((prev) =>
      prev.map((task) => {
        if (task.id === taskId) {
          // Toggle the status
          const statuses = ["completed", "in-progress", "pending", "need-help", "failed"];
          const currentIndex = Math.floor(Math.random() * statuses.length);
          const newStatus = statuses[currentIndex];

          // If task is now completed, mark all subtasks as completed
          const updatedSubtasks = task.subtasks.map((subtask) => ({
            ...subtask,
            status: newStatus === "completed" ? "completed" : subtask.status,
          }));

          return {
            ...task,
            status: newStatus,
            subtasks: updatedSubtasks,
          };
        }
        return task;
      }),
    );
  };

  // Toggle subtask status
  const toggleSubtaskStatus = (taskId: string, subtaskId: string) => {
    setTasks((prev) =>
      prev.map((task) => {
        if (task.id === taskId) {
          const updatedSubtasks = task.subtasks.map((subtask) => {
            if (subtask.id === subtaskId) {
              const newStatus =
                subtask.status === "completed" ? "pending" : "completed";
              return { ...subtask, status: newStatus };
            }
            return subtask;
          });

          // Calculate if task should be auto-completed when all subtasks are done
          const allSubtasksCompleted = updatedSubtasks.every(
            (s) => s.status === "completed",
          );

          return {
            ...task,
            subtasks: updatedSubtasks,
            status: allSubtasksCompleted ? "completed" : task.status,
          };
        }
        return task;
      }),
    );
  };

  // Animation variants with reduced motion support
  const taskVariants = {
    hidden: { 
      opacity: 0, 
      y: prefersReducedMotion ? 0 : -5 
    },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { 
        type: prefersReducedMotion ? "tween" : "spring", 
        stiffness: 500, 
        damping: 30,
        duration: prefersReducedMotion ? 0.2 : undefined
      }
    },
    exit: {
      opacity: 0,
      y: prefersReducedMotion ? 0 : -5,
      transition: { duration: 0.15 }
    }
  };

  const subtaskListVariants = {
    hidden: { 
      opacity: 0, 
      height: 0,
      overflow: "hidden" 
    },
    visible: { 
      height: "auto", 
      opacity: 1,
      overflow: "visible",
      transition: { 
        duration: 0.25, 
        staggerChildren: prefersReducedMotion ? 0 : 0.05,
        when: "beforeChildren",
        ease: [0.2, 0.65, 0.3, 0.9] // Custom easing curve for Apple-like feel
      }
    },
    exit: {
      height: 0,
      opacity: 0,
      overflow: "hidden",
      transition: { 
        duration: 0.2,
        ease: [0.2, 0.65, 0.3, 0.9]
      }
    }
  };

  const subtaskVariants = {
    hidden: { 
      opacity: 0, 
      x: prefersReducedMotion ? 0 : -10 
    },
    visible: { 
      opacity: 1, 
      x: 0,
      transition: { 
        type: prefersReducedMotion ? "tween" : "spring", 
        stiffness: 500, 
        damping: 25,
        duration: prefersReducedMotion ? 0.2 : undefined
      }
    },
    exit: {
      opacity: 0,
      x: prefersReducedMotion ? 0 : -10,
      transition: { duration: 0.15 }
    }
  };

  const subtaskDetailsVariants = {
    hidden: { 
      opacity: 0, 
      height: 0,
      overflow: "hidden"
    },
    visible: { 
      opacity: 1, 
      height: "auto",
      overflow: "visible",
      transition: { 
        duration: 0.25,
        ease: [0.2, 0.65, 0.3, 0.9]
      }
    }
  };

  // Status badge animation variants
  const statusBadgeVariants = {
    initial: { scale: 1 },
    animate: { 
      scale: prefersReducedMotion ? 1 : [1, 1.08, 1],
      transition: { 
        duration: 0.35,
        ease: [0.34, 1.56, 0.64, 1] // Springy custom easing for bounce effect
      }
    }
  };

  return (
    <div className="bg-background text-foreground h-full overflow-auto p-2">
      <motion.div 
        className="bg-card border-border rounded-lg border shadow overflow-hidden"
        initial={{ opacity: 0, y: 10 }}
        animate={{ 
          opacity: 1, 
          y: 0,
          transition: {
            duration: 0.3,
            ease: [0.2, 0.65, 0.3, 0.9]
          }
        }}
      >
        <LayoutGroup>
          <div className="p-4 overflow-hidden">
            <ul className="space-y-1 overflow-hidden">
              {tasks.map((task, index) => {
                const isExpanded = expandedTasks.includes(task.id);
                const isCompleted = task.status === "completed";

                return (
                  <motion.li
                    key={task.id}
                    className={` ${index !== 0 ? "mt-1 pt-2" : ""} `}
                    initial="hidden"
                    animate="visible"
                    variants={taskVariants}
                  >
                    {/* Task row */}
                    <motion.div 
                      className="group flex items-center px-3 py-1.5 rounded-md"
                      whileHover={{ 
                        backgroundColor: "rgba(0,0,0,0.03)",
                        transition: { duration: 0.2 }
                      }}
                    >
                      <motion.div
                        className="mr-2 flex-shrink-0 cursor-pointer"
                        onClick={(e) => {
                          e.stopPropagation();
                          toggleTaskStatus(task.id);
                        }}
                        whileTap={{ scale: 0.9 }}
                        whileHover={{ scale: 1.1 }}
                      >
                        <AnimatePresence mode="wait">
                          <motion.div
                            key={task.status}
                            initial={{ opacity: 0, scale: 0.8, rotate: -10 }}
                            animate={{ opacity: 1, scale: 1, rotate: 0 }}
                            exit={{ opacity: 0, scale: 0.8, rotate: 10 }}
                            transition={{
                              duration: 0.2,
                              ease: [0.2, 0.65, 0.3, 0.9]
                            }}
                          >
                            {task.status === "completed" ? (
                              <CheckCircle2 className="h-4.5 w-4.5 text-green-500" />
                            ) : task.status === "in-progress" ? (
                              <CircleDotDashed className="h-4.5 w-4.5 text-blue-500" />
                            ) : task.status === "need-help" ? (
                              <CircleAlert className="h-4.5 w-4.5 text-yellow-500" />
                            ) : task.status === "failed" ? (
                              <CircleX className="h-4.5 w-4.5 text-red-500" />
                            ) : (
                              <Circle className="text-muted-foreground h-4.5 w-4.5" />
                            )}
                          </motion.div>
                        </AnimatePresence>
                      </motion.div>

                      <motion.div
                        className="flex min-w-0 flex-grow cursor-pointer items-center justify-between"
                        onClick={() => toggleTaskExpansion(task.id)}
                      >
                        <div className="mr-2 flex-1 truncate">
                          <span
                            className={`${isCompleted ? "text-muted-foreground line-through" : ""}`}
                          >
                            {task.title}
                          </span>
                        </div>

                        <div className="flex flex-shrink-0 items-center space-x-2 text-xs">
                          {task.dependencies.length > 0 && (
                            <div className="flex items-center mr-2">
                              <div className="flex flex-wrap gap-1">
                                {task.dependencies.map((dep, idx) => (
                                  <motion.span
                                    key={idx}
                                    className="bg-secondary/40 text-secondary-foreground rounded px-1.5 py-0.5 text-[10px] font-medium shadow-sm"
                                    initial={{ opacity: 0, scale: 0.9 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    transition={{
                                      duration: 0.2,
                                      delay: idx * 0.05
                                    }}
                                    whileHover={{ 
                                      y: -1, 
                                      backgroundColor: "rgba(0,0,0,0.1)",
                                      transition: { duration: 0.2 } 
                                    }}
                                  >
                                    {dep}
                                  </motion.span>
                                ))}
                              </div>
                            </div>
                          )}

                          <motion.span
                            className={`rounded px-1.5 py-0.5 ${
                              task.status === "completed"
                                ? "bg-green-100 text-green-700"
                                : task.status === "in-progress"
                                  ? "bg-blue-100 text-blue-700"
                                  : task.status === "need-help"
                                    ? "bg-yellow-100 text-yellow-700"
                                    : task.status === "failed"
                                      ? "bg-red-100 text-red-700"
                                      : "bg-muted text-muted-foreground"
                            }`}
                            variants={statusBadgeVariants}
                            initial="initial"
                            animate="animate"
                            key={task.status} // Force animation on status change
                          >
                            {task.status}
                          </motion.span>
                        </div>
                      </motion.div>
                    </motion.div>

                    {/* Subtasks - staggered */}
                    <AnimatePresence mode="wait">
                      {isExpanded && task.subtasks.length > 0 && (
                        <motion.div 
                          className="relative overflow-hidden"
                          variants={subtaskListVariants}
                          initial="hidden"
                          animate="visible"
                          exit="hidden"
                          layout
                        >
                          {/* Vertical connecting line aligned with task icon */}
                          <div className="absolute top-0 bottom-0 left-[20px] border-l-2 border-dashed border-muted-foreground/30" />
                          <ul className="border-muted mt-1 mr-2 mb-1.5 ml-3 space-y-0.5">
                            {task.subtasks.map((subtask) => {
                              const subtaskKey = `${task.id}-${subtask.id}`;
                              const isSubtaskExpanded = expandedSubtasks[subtaskKey];

                              return (
                                <motion.li
                                  key={subtask.id}
                                  className="group flex flex-col py-0.5 pl-6"
                                  onClick={() =>
                                    toggleSubtaskExpansion(task.id, subtask.id)
                                  }
                                  variants={subtaskVariants}
                                  initial="hidden"
                                  animate="visible"
                                  exit="exit"
                                  layout
                                >
                                  <motion.div 
                                    className="flex flex-1 items-center rounded-md p-1"
                                    whileHover={{ 
                                      backgroundColor: "rgba(0,0,0,0.03)",
                                      transition: { duration: 0.2 }
                                    }}
                                    layout
                                  >
                                    <motion.div
                                      className="mr-2 flex-shrink-0 cursor-pointer"
                                      onClick={(e) => {
                                        e.stopPropagation();
                                        toggleSubtaskStatus(task.id, subtask.id);
                                      }}
                                      whileTap={{ scale: 0.9 }}
                                      whileHover={{ scale: 1.1 }}
                                      layout
                                    >
                                      <AnimatePresence mode="wait">
                                        <motion.div
                                          key={subtask.status}
                                          initial={{ opacity: 0, scale: 0.8, rotate: -10 }}
                                          animate={{ opacity: 1, scale: 1, rotate: 0 }}
                                          exit={{ opacity: 0, scale: 0.8, rotate: 10 }}
                                          transition={{
                                            duration: 0.2,
                                            ease: [0.2, 0.65, 0.3, 0.9]
                                          }}
                                        >
                                          {subtask.status === "completed" ? (
                                            <CheckCircle2 className="h-3.5 w-3.5 text-green-500" />
                                          ) : subtask.status === "in-progress" ? (
                                            <CircleDotDashed className="h-3.5 w-3.5 text-blue-500" />
                                          ) : subtask.status === "need-help" ? (
                                            <CircleAlert className="h-3.5 w-3.5 text-yellow-500" />
                                          ) : subtask.status === "failed" ? (
                                            <CircleX className="h-3.5 w-3.5 text-red-500" />
                                          ) : (
                                            <Circle className="text-muted-foreground h-3.5 w-3.5" />
                                          )}
                                        </motion.div>
                                      </AnimatePresence>
                                    </motion.div>

                                    <span
                                      className={`cursor-pointer text-sm ${subtask.status === "completed" ? "text-muted-foreground line-through" : ""}`}
                                    >
                                      {subtask.title}
                                    </span>
                                  </motion.div>

                                  <AnimatePresence mode="wait">
                                    {isSubtaskExpanded && (
                                      <motion.div 
                                        className="text-muted-foreground border-foreground/20 mt-1 ml-1.5 border-l border-dashed pl-5 text-xs overflow-hidden"
                                        variants={subtaskDetailsVariants}
                                        initial="hidden"
                                        animate="visible"
                                        exit="hidden"
                                        layout
                                      >
                                        <p className="py-1">{subtask.description}</p>
                                        {subtask.tools && subtask.tools.length > 0 && (
                                          <div className="mt-0.5 mb-1 flex flex-wrap items-center gap-1.5">
                                            <span className="text-muted-foreground font-medium">
                                              MCP Servers:
                                            </span>
                                            <div className="flex flex-wrap gap-1">
                                              {subtask.tools.map((tool, idx) => (
                                                <motion.span
                                                  key={idx}
                                                  className="bg-secondary/40 text-secondary-foreground rounded px-1.5 py-0.5 text-[10px] font-medium shadow-sm"
                                                  initial={{ opacity: 0, y: -5 }}
                                                  animate={{ 
                                                    opacity: 1, 
                                                    y: 0,
                                                    transition: {
                                                      duration: 0.2,
                                                      delay: idx * 0.05
                                                    }
                                                  }}
                                                  whileHover={{ 
                                                    y: -1, 
                                                    backgroundColor: "rgba(0,0,0,0.1)",
                                                    transition: { duration: 0.2 } 
                                                  }}
                                                >
                                                  {tool}
                                                </motion.span>
                                              ))}
                                            </div>
                                          </div>
                                        )}
                                      </motion.div>
                                    )}
                                  </AnimatePresence>
                                </motion.li>
                              );
                            })}
                          </ul>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </motion.li>
                );
              })}
            </ul>
          </div>
        </LayoutGroup>
      </motion.div>
    </div>
  );
}


demo.tsx
"use client";

import Plan from "@/components/ui/agent-plan";

export function Demo() {
  return (
    <div className="flex flex-col p-4 w-full h-full">
      <Plan />
    </div>
  );
}

```

Install NPM dependencies:
```bash
lucide-react, framer-motion
```

Implementation Guidelines
 1. Analyze the component structure and identify all required dependencies
 2. Review the component's argumens and state
 3. Identify any required context providers or hooks and install them
 4. Questions to Ask
 - What data/props will be passed to this component?
 - Are there any specific state management requirements?
 - Are there any required assets (images, icons, etc.)?
 - What is the expected responsive behavior?
 - What is the best place to use this component in the app?

Steps to integrate
 0. Copy paste all the code above in the correct directories
 1. Install external dependencies
 2. Fill image assets with Unsplash stock images you know exist
 3. Use lucide-react icons for svgs or logos if component requires them

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


