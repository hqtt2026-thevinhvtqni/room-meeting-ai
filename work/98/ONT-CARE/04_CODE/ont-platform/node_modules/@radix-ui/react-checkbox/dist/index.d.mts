import * as _radix_ui_react_context from '@radix-ui/react-context';
import { Scope } from '@radix-ui/react-context';
import * as React from 'react';
import { Primitive } from '@radix-ui/react-primitive';

type ScopedProps<P> = P & {
    __scopeCheckbox?: Scope | undefined;
};
declare const createCheckboxScope: _radix_ui_react_context.CreateScope;
type CheckedState = boolean | 'indeterminate';
interface CheckboxProviderProps<State extends CheckedState = CheckedState> {
    checked?: State | boolean | undefined;
    defaultChecked?: State | boolean | undefined;
    required?: boolean | undefined;
    onCheckedChange?: {
        bivarianceHack(checked: State | boolean): void;
    }['bivarianceHack'] | undefined;
    name?: string | undefined;
    form?: string | undefined;
    disabled?: boolean | undefined;
    value?: string | number | readonly string[] | undefined;
    children?: React.ReactNode | undefined;
}
declare function CheckboxProvider<State extends CheckedState = CheckedState>(props: ScopedProps<CheckboxProviderProps<State>>): React.JSX.Element;
interface CheckboxTriggerProps extends Omit<React.ComponentPropsWithoutRef<typeof Primitive.button>, keyof CheckboxProviderProps> {
    children?: React.ReactNode | undefined;
}
declare const CheckboxTrigger: React.ForwardRefExoticComponent<CheckboxTriggerProps & React.RefAttributes<HTMLButtonElement>>;
type PrimitiveButtonProps = React.ComponentPropsWithoutRef<typeof Primitive.button>;
interface CheckboxProps extends Omit<PrimitiveButtonProps, 'checked' | 'defaultChecked'> {
    checked?: CheckedState | undefined;
    defaultChecked?: CheckedState | undefined;
    required?: boolean | undefined;
    onCheckedChange?: {
        bivarianceHack(checked: CheckedState): void;
    }['bivarianceHack'] | undefined;
}
declare const Checkbox: React.ForwardRefExoticComponent<CheckboxProps & React.RefAttributes<HTMLButtonElement>>;
type PrimitiveSpanProps = React.ComponentPropsWithoutRef<typeof Primitive.span>;
interface CheckboxIndicatorProps extends PrimitiveSpanProps {
    /**
     * Used to force mounting when more control is needed. Useful when
     * controlling animation with React animation libraries.
     */
    forceMount?: true | undefined;
}
declare const CheckboxIndicator: React.ForwardRefExoticComponent<CheckboxIndicatorProps & React.RefAttributes<HTMLSpanElement>>;
type InputProps = React.ComponentPropsWithoutRef<typeof Primitive.input>;
interface CheckboxBubbleInputProps extends Omit<InputProps, 'checked'> {
}
declare const CheckboxBubbleInput: React.ForwardRefExoticComponent<CheckboxBubbleInputProps & React.RefAttributes<HTMLInputElement>>;

export { Checkbox, CheckboxIndicator, type CheckboxIndicatorProps, type CheckboxProps, type CheckedState, CheckboxIndicator as Indicator, Checkbox as Root, createCheckboxScope, CheckboxBubbleInput as unstable_BubbleInput, CheckboxBubbleInput as unstable_CheckboxBubbleInput, type CheckboxBubbleInputProps as unstable_CheckboxBubbleInputProps, CheckboxProvider as unstable_CheckboxProvider, type CheckboxProviderProps as unstable_CheckboxProviderProps, CheckboxTrigger as unstable_CheckboxTrigger, type CheckboxTriggerProps as unstable_CheckboxTriggerProps, CheckboxProvider as unstable_Provider, CheckboxTrigger as unstable_Trigger };
