import * as _radix_ui_react_context from '@radix-ui/react-context';
import { Scope } from '@radix-ui/react-context';
import * as React from 'react';
import { Primitive } from '@radix-ui/react-primitive';

type ScopedProps<P> = P & {
    __scopeSwitch?: Scope | undefined;
};
declare const createSwitchScope: _radix_ui_react_context.CreateScope;
interface SwitchProviderProps {
    checked?: boolean | undefined;
    defaultChecked?: boolean | undefined;
    required?: boolean | undefined;
    onCheckedChange?: {
        bivarianceHack(checked: boolean): void;
    }['bivarianceHack'] | undefined;
    name?: string | undefined;
    form?: string | undefined;
    disabled?: boolean | undefined;
    value?: string | number | readonly string[] | undefined;
    children?: React.ReactNode | undefined;
}
declare function SwitchProvider(props: ScopedProps<SwitchProviderProps>): React.JSX.Element;
interface SwitchTriggerProps extends Omit<React.ComponentPropsWithoutRef<typeof Primitive.button>, keyof SwitchProviderProps> {
    children?: React.ReactNode | undefined;
}
declare const SwitchTrigger: React.ForwardRefExoticComponent<SwitchTriggerProps & React.RefAttributes<HTMLButtonElement>>;
type PrimitiveButtonProps = React.ComponentPropsWithoutRef<typeof Primitive.button>;
interface SwitchProps extends Omit<PrimitiveButtonProps, 'checked' | 'defaultChecked'> {
    checked?: boolean | undefined;
    defaultChecked?: boolean | undefined;
    required?: boolean | undefined;
    onCheckedChange?: {
        bivarianceHack(checked: boolean): void;
    }['bivarianceHack'] | undefined;
}
declare const Switch: React.ForwardRefExoticComponent<SwitchProps & React.RefAttributes<HTMLButtonElement>>;
type PrimitiveSpanProps = React.ComponentPropsWithoutRef<typeof Primitive.span>;
interface SwitchThumbProps extends PrimitiveSpanProps {
}
declare const SwitchThumb: React.ForwardRefExoticComponent<SwitchThumbProps & React.RefAttributes<HTMLSpanElement>>;
type InputProps = React.ComponentPropsWithoutRef<typeof Primitive.input>;
interface SwitchBubbleInputProps extends Omit<InputProps, 'checked'> {
}
declare const SwitchBubbleInput: React.ForwardRefExoticComponent<SwitchBubbleInputProps & React.RefAttributes<HTMLInputElement>>;

export { Switch as Root, Switch, type SwitchProps, SwitchThumb, type SwitchThumbProps, SwitchThumb as Thumb, createSwitchScope, SwitchBubbleInput as unstable_BubbleInput, SwitchProvider as unstable_Provider, SwitchBubbleInput as unstable_SwitchBubbleInput, type SwitchBubbleInputProps as unstable_SwitchBubbleInputProps, SwitchProvider as unstable_SwitchProvider, type SwitchProviderProps as unstable_SwitchProviderProps, SwitchTrigger as unstable_SwitchTrigger, type SwitchTriggerProps as unstable_SwitchTriggerProps, SwitchTrigger as unstable_Trigger };
