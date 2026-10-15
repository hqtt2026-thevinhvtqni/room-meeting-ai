import * as _radix_ui_react_context from '@radix-ui/react-context';
import * as React from 'react';
import { Primitive } from '@radix-ui/react-primitive';
import * as RovingFocusGroup from '@radix-ui/react-roving-focus';

declare const ActivationMode: {
    readonly Automatic: "automatic";
    readonly Manual: "manual";
};
type ActivationMode = (typeof ActivationMode)[keyof typeof ActivationMode];
declare const createTabsScope: _radix_ui_react_context.CreateScope;
type RovingFocusGroupProps = React.ComponentPropsWithoutRef<typeof RovingFocusGroup.Root>;
type PrimitiveDivProps = React.ComponentPropsWithoutRef<typeof Primitive.div>;
interface TabsProps extends PrimitiveDivProps {
    /** The value for the selected tab, if controlled */
    value?: string | undefined;
    /** The value of the tab to select by default, if uncontrolled */
    defaultValue?: string | undefined;
    /** A function called when a new tab is selected */
    onValueChange?: {
        bivarianceHack(value: string): void;
    }['bivarianceHack'] | undefined;
    /**
     * The orientation the tabs are layed out.
     * Mainly so arrow navigation is done accordingly (left & right vs. up & down)
     * @defaultValue horizontal
     */
    orientation?: RovingFocusGroupProps['orientation'] | undefined;
    /**
     * The direction of navigation between toolbar items.
     */
    dir?: RovingFocusGroupProps['dir'] | undefined;
    /**
     * Whether a tab is activated automatically or manually.
     * @defaultValue automatic
     * */
    activationMode?: ActivationMode | undefined;
}
declare const Tabs: React.ForwardRefExoticComponent<TabsProps & React.RefAttributes<HTMLDivElement>>;
interface TabsListProps extends PrimitiveDivProps {
    loop?: RovingFocusGroupProps['loop'] | undefined;
}
declare const TabsList: React.ForwardRefExoticComponent<TabsListProps & React.RefAttributes<HTMLDivElement>>;
type PrimitiveButtonProps = React.ComponentPropsWithoutRef<typeof Primitive.button>;
interface TabsTriggerProps extends PrimitiveButtonProps {
    value: string;
}
declare const TabsTrigger: React.ForwardRefExoticComponent<TabsTriggerProps & React.RefAttributes<HTMLButtonElement>>;
interface TabsContentProps extends PrimitiveDivProps {
    value: string;
    /**
     * Used to force mounting when more control is needed. Useful when
     * controlling animation with React animation libraries.
     */
    forceMount?: true | undefined;
}
declare const TabsContent: React.ForwardRefExoticComponent<TabsContentProps & React.RefAttributes<HTMLDivElement>>;

export { TabsContent as Content, TabsList as List, Tabs as Root, Tabs, TabsContent, type TabsContentProps, TabsList, type TabsListProps, type TabsProps, TabsTrigger, type TabsTriggerProps, TabsTrigger as Trigger, createTabsScope };
