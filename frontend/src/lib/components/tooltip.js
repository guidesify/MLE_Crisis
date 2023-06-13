import Tooltip from './TooltipFromAction.svelte';

export function tooltip(element) {
	let div;
	let title_custom;
	let tooltipComponent;
	function mouseOver(event) {
		// NOTE: remove the `title` attribute, to prevent showing the default browser tooltip
		// remember to set it back on `mouseleave`
		title_custom = element.getAttribute('title_custom');
		element.removeAttribute('title_custom');

		tooltipComponent = new Tooltip({
			props: {
				title_custom: title_custom,
				x: event.pageX,
				y: event.pageY,
			},
			target: document.body,
		});
	}
	function mouseMove(event) {
		tooltipComponent.$set({
			x: event.pageX,
			y: event.pageY,
		})
	}
	function mouseLeave() {
		tooltipComponent.$destroy();
		// NOTE: restore the `title` attribute
		element.setAttribute('title_custom', title_custom);
	}
	
	element.addEventListener('mouseover', mouseOver);
  element.addEventListener('mouseleave', mouseLeave);
	element.addEventListener('mousemove', mouseMove);
	
	return {
		destroy() {
			element.removeEventListener('mouseover', mouseOver);
			element.removeEventListener('mouseleave', mouseLeave);
			element.removeEventListener('mousemove', mouseMove);
		}
	}
}