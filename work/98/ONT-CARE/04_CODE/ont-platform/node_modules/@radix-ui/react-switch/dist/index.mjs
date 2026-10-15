"use client";
var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// src/switch.tsx
import * as React from "react";
import { composeEventHandlers } from "@radix-ui/primitive";
import { useComposedRefs } from "@radix-ui/react-compose-refs";
import { createContextScope } from "@radix-ui/react-context";
import { useControllableState } from "@radix-ui/react-use-controllable-state";
import { useSize } from "@radix-ui/react-use-size";
import { Primitive } from "@radix-ui/react-primitive";
import { Fragment, jsx, jsxs } from "react/jsx-runtime";
var SWITCH_NAME = "Switch";
var [createSwitchContext, createSwitchScope] = createContextScope(SWITCH_NAME);
var [SwitchProviderImpl, useSwitchContext] = createSwitchContext(SWITCH_NAME);
function SwitchProvider(props) {
  const {
    __scopeSwitch,
    checked: checkedProp,
    children,
    defaultChecked,
    disabled,
    form,
    name,
    onCheckedChange,
    required,
    value = "on",
    // @ts-expect-error
    internal_do_not_use_render
  } = props;
  const [checked, setChecked] = useControllableState({
    prop: checkedProp,
    defaultProp: defaultChecked ?? false,
    onChange: onCheckedChange,
    caller: SWITCH_NAME
  });
  const [control, setControl] = React.useState(null);
  const [bubbleInput, setBubbleInput] = React.useState(null);
  const [userClick, setUserClick] = React.useState(null);
  const isFormControl = control ? !!form || !!control.closest("form") : (
    // We set this to true by default so that events bubble to forms without JS (SSR)
    true
  );
  const context = {
    checked,
    setChecked,
    disabled,
    control,
    setControl,
    name,
    form,
    value,
    userClick,
    onUserClick: setUserClick,
    required,
    defaultChecked,
    isFormControl,
    bubbleInput,
    setBubbleInput
  };
  return /* @__PURE__ */ jsx(SwitchProviderImpl, { scope: __scopeSwitch, ...context, children: isFunction(internal_do_not_use_render) ? internal_do_not_use_render(context) : children });
}
__name(SwitchProvider, "SwitchProvider");
var TRIGGER_NAME = "SwitchTrigger";
var SwitchTrigger = /* @__PURE__ */ React.forwardRef(
  /* @__PURE__ */ __name(function SwitchTrigger2({ __scopeSwitch, onClick, ...switchProps }, forwardedRef) {
    const {
      control,
      form,
      value,
      disabled,
      checked,
      required,
      setControl,
      setChecked,
      onUserClick,
      isFormControl,
      bubbleInput
    } = useSwitchContext(TRIGGER_NAME, __scopeSwitch);
    const composedRefs = useComposedRefs(forwardedRef, setControl);
    const initialCheckedStateRef = React.useRef(checked);
    React.useEffect(() => {
      const associatedForm = form ? control?.ownerDocument.getElementById(form) : control?.form;
      if (associatedForm instanceof HTMLFormElement) {
        const reset = /* @__PURE__ */ __name(() => setChecked(initialCheckedStateRef.current), "reset");
        associatedForm.addEventListener("reset", reset);
        return () => associatedForm.removeEventListener("reset", reset);
      }
    }, [control, form, setChecked]);
    return /* @__PURE__ */ jsx(
      Primitive.button,
      {
        type: "button",
        role: "switch",
        "aria-checked": checked,
        "aria-required": required,
        "data-state": getState(checked),
        "data-disabled": disabled ? "" : void 0,
        disabled,
        value,
        ...switchProps,
        ref: composedRefs,
        onClick: composeEventHandlers(onClick, (event) => {
          const hasConsumerStoppedPropagation = event.isPropagationStopped();
          onUserClick({ requestedChecked: !checked, hasConsumerStoppedPropagation });
          setChecked((prevChecked) => !prevChecked);
          if (bubbleInput && isFormControl) {
            if (!hasConsumerStoppedPropagation) {
              event.stopPropagation();
            }
          }
        })
      }
    );
  }, "SwitchTrigger")
);
var Switch = /* @__PURE__ */ React.forwardRef(
  // blank line to reduce diff noise
  /* @__PURE__ */ __name(function Switch2(props, forwardedRef) {
    const {
      __scopeSwitch,
      name,
      checked,
      defaultChecked,
      required,
      disabled,
      value,
      onCheckedChange,
      form,
      ...switchProps
    } = props;
    return /* @__PURE__ */ jsx(
      SwitchProvider,
      {
        __scopeSwitch,
        checked,
        defaultChecked,
        disabled,
        required,
        onCheckedChange,
        name,
        form,
        value,
        internal_do_not_use_render: ({ isFormControl }) => /* @__PURE__ */ jsxs(Fragment, { children: [
          /* @__PURE__ */ jsx(
            SwitchTrigger,
            {
              ...switchProps,
              ref: forwardedRef,
              __scopeSwitch
            }
          ),
          isFormControl && /* @__PURE__ */ jsx(
            SwitchBubbleInput,
            {
              __scopeSwitch
            }
          )
        ] })
      }
    );
  }, "Switch")
);
var THUMB_NAME = "SwitchThumb";
var SwitchThumb = /* @__PURE__ */ React.forwardRef(
  /* @__PURE__ */ __name(function SwitchThumb2(props, forwardedRef) {
    const { __scopeSwitch, ...thumbProps } = props;
    const context = useSwitchContext(THUMB_NAME, __scopeSwitch);
    return /* @__PURE__ */ jsx(
      Primitive.span,
      {
        "data-state": getState(context.checked),
        "data-disabled": context.disabled ? "" : void 0,
        ...thumbProps,
        ref: forwardedRef
      }
    );
  }, "SwitchThumb")
);
var BUBBLE_INPUT_NAME = "SwitchBubbleInput";
var SwitchBubbleInput = /* @__PURE__ */ React.forwardRef(
  // blank line to reduce diff noise
  /* @__PURE__ */ __name(function SwitchBubbleInput2({ __scopeSwitch, onClick, ...props }, forwardedRef) {
    const {
      control,
      userClick,
      checked,
      defaultChecked,
      required,
      disabled,
      name,
      value,
      form,
      bubbleInput,
      setBubbleInput
    } = useSwitchContext(BUBBLE_INPUT_NAME, __scopeSwitch);
    const composedRefs = useComposedRefs(forwardedRef, setBubbleInput);
    const controlSize = useSize(control);
    const shouldStopClickPropagationRef = React.useRef(false);
    const prevCheckedRef = React.useRef(checked);
    const handledUserClickRef = React.useRef(userClick);
    const pendingUserClickRef = React.useRef(null);
    React.useEffect(() => {
      const input = bubbleInput;
      if (!input) return;
      const inputProto = window.HTMLInputElement.prototype;
      const descriptor = Object.getOwnPropertyDescriptor(
        inputProto,
        "checked"
      );
      const setChecked = descriptor.set;
      if (!setChecked) {
        return;
      }
      const checkedChanged = prevCheckedRef.current !== checked;
      prevCheckedRef.current = checked;
      const isNewUserClick = userClick !== null && userClick !== handledUserClickRef.current;
      handledUserClickRef.current = userClick;
      if (isNewUserClick) {
        pendingUserClickRef.current = checkedChanged ? null : userClick;
        if (checkedChanged) {
          setChecked.call(input, checked);
        }
        input.dispatchEvent(
          new Event("click", { bubbles: !userClick.hasConsumerStoppedPropagation })
        );
      } else if (checkedChanged) {
        const pendingUserClick = pendingUserClickRef.current;
        pendingUserClickRef.current = null;
        const isPendingUserChange = pendingUserClick?.requestedChecked === checked;
        shouldStopClickPropagationRef.current = true;
        setChecked.call(input, checked);
        input.dispatchEvent(
          new Event("click", {
            bubbles: !(isPendingUserChange && pendingUserClick.hasConsumerStoppedPropagation)
          })
        );
        shouldStopClickPropagationRef.current = false;
      }
    }, [bubbleInput, checked, userClick]);
    const defaultCheckedRef = React.useRef(checked);
    return /* @__PURE__ */ jsx(
      Primitive.input,
      {
        type: "checkbox",
        "aria-hidden": true,
        defaultChecked: defaultChecked ?? defaultCheckedRef.current,
        required,
        disabled,
        name,
        value,
        form,
        ...props,
        tabIndex: -1,
        ref: composedRefs,
        onClick: composeEventHandlers(onClick, (event) => {
          if (shouldStopClickPropagationRef.current) {
            event.stopPropagation();
          }
        }),
        style: {
          ...props.style,
          ...controlSize,
          position: "absolute",
          pointerEvents: "none",
          opacity: 0,
          margin: 0,
          // We transform because the input is absolutely positioned but we have
          // rendered it **after** the button. This pulls it back to sit on top
          // of the button.
          transform: "translateX(-100%)"
        }
      }
    );
  }, "SwitchBubbleInput")
);
function isFunction(value) {
  return typeof value === "function";
}
__name(isFunction, "isFunction");
function getState(checked) {
  return checked ? "checked" : "unchecked";
}
__name(getState, "getState");
export {
  Switch as Root,
  Switch,
  SwitchThumb,
  SwitchThumb as Thumb,
  createSwitchScope,
  SwitchBubbleInput as unstable_BubbleInput,
  SwitchProvider as unstable_Provider,
  SwitchBubbleInput as unstable_SwitchBubbleInput,
  SwitchProvider as unstable_SwitchProvider,
  SwitchTrigger as unstable_SwitchTrigger,
  SwitchTrigger as unstable_Trigger
};
//# sourceMappingURL=index.mjs.map
