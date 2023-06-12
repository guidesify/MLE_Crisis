<script>
    export let label;
    export let loading = false;
    export let disabled = false;
    export let primary = false;
    export let secondary = false;
    export let danger = false;
    export let success = false;
    export let link = false;
    export let tiny = false;
    export let small = false;
    export let medium = false;
    export let large = false;
    export let wide = false;
    export let nowrap = true;
    export let active = false;
  
      const httpRegex = /^((http|https):\/\/)/;
  
    export let href = undefined;
    export let tag = href ? 'a' : 'button';
    export let external = !!href && httpRegex.test(href);
    export let target = external ? '_blank' : undefined;
    export let rel = external ? 'noopener noreferrer' : undefined;    
    const roundrect = primary || secondary || danger || success;
  </script>
  
  <svelte:element
      this={tag}
      data-sveltekit-preload-data={external ? 'hover' : 'off' }
    {href}
    {rel}
    {target}
      aria-label={label}
      class="button"
      class:roundrect
      class:link
      class:primary
      class:secondary
      class:danger
      class:success
      class:loading
      class:tiny
      class:small
      class:medium
      class:large
      class:wide
      class:nowrap
      class:active
      disabled={loading || disabled}
      on:click
      on:keydown
  >
    <slot>{label}</slot>
  </svelte:element>
  
  <style>
      .button {
      cursor: pointer;
      appearance: none;
      text-align: inherit;
      font-size: inherit;
      line-height: inherit;
      background-color: transparent;
      border: none;
      color: inherit;
      padding: 0;
      margin: 0;
      width: auto;
      height: auto;
      display: inline-block;
      font-family: inherit;
      font-size: inherit;
      font-weight: inherit;
      position: relative;
      vertical-align: baseline;
      box-sizing: border-box;
      text-align: center;
      }
  
      .button.nowrap {
          white-space: nowrap;
      }
      
      :global(a).button {
          text-decoration: none;
      }
      
      .button.link {
          color: rebeccapurple;
          text-decoration: underline;
      }
      
      .button.roundrect {
          font-weight: bold;
          padding: 0.4em 1.2em;
          border-radius: 8px;
          box-sizing: border-box;
          color: var(--text-color);
          background-color: var(--background-color);
          border: 1px solid var(--border-color);
          box-shadow: 0px 1px 0 var(--shadow-color);
          transform: translateY(0);
          font-size: 0.9em;
      }
      .button.roundrect:active {
          box-shadow: none;
          transform: translateY(1px);
      }
      
      .button.roundrect.primary {
          --text-color: white;
          --background-color: rgb(59 130 246);
          --border-color: none;
          --shadow-color: #00000011;
          transition: background-color 0.2s ease, box-shadow 0.2s ease;
      }

      .button.roundrect.primary:hover {
        --tw-ring-color: rgb(14, 97, 231);
        --tw-ring-offset-color: rgb(33, 108, 230);
        --tw-ring-inset: var(--tw-empty,/*!*/ /*!*/);
        box-shadow: var(--tw-ring-inset) 0 0 0 calc(3px + var(--tw-ring-offset-width)) var(--tw-ring-color);
        }
  
      .button.roundrect.secondary {
            --text-color: #2e2e2e;
            --background-color: white;
            --border-color: transparent;
            --shadow-color: #00000011;
            transition: background-color 0.2s ease, box-shadow 0.2s ease;
            }

        .button.roundrect.secondary:hover {
        border-color: #93c9ec;
        box-shadow: var(--tw-ring-inset) 0 0 0 calc(3px + var(--tw-ring-offset-width)) var(--tw-ring-color);
        }

        .button.roundrect.danger {
            --text-color: rgba(255, 255, 255, 0.837);
            --background-color: rgb(200, 30, 30);
            --border-color: transparent;
            --shadow-color: #00000011;
            transition: background-color 0.2s ease, box-shadow 0.2s ease;
            }

        .button.roundrect.danger:hover {
        --tw-ring-color: rgba(231, 14, 14, 0.463);
        --tw-ring-offset-color: rgba(230, 33, 33, 0.753);
        --tw-ring-inset: var(--tw-empty,/*!*/ /*!*/);
        border-color: transparent;
        box-shadow: var(--tw-ring-inset) 0 0 0 calc(3px + var(--tw-ring-offset-width)) var(--tw-ring-color);
        }

              /* disabled */
        .button.roundrect:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        --background-color: #dad9d9;
        --text-color: #7e7e7e;
    }
      
      :global(select).button.roundrect {
          background-image: url('data:image/svg+xml;charset=utf-8,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22%2300000099%22%3E%3Cpath%20d%3D%22M11.3%2C14.3c0.4%2C0.4%2C1%2C0.4%2C1.4%2C0l4.6-4.6C17.7%2C9.3%2C17.5%2C9%2C17%2C9H7C6.4%2C9%2C6.3%2C9.3%2C6.7%2C9.7L11.3%2C14.3z%22%2F%3E%3C%2Fsvg%3E');
          background-repeat: no-repeat;
          background-position: calc(100% - 0.33em) 50%;
          background-size: 1.75em;
          padding-right: 3em;
      }
  
      :global(select).button.roundrect.primary {
          background-image: url('data:image/svg+xml;charset=utf-8,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22%23ffffffdd%22%3E%3Cpath%20d%3D%22M11.3%2C14.3c0.4%2C0.4%2C1%2C0.4%2C1.4%2C0l4.6-4.6C17.7%2C9.3%2C17.5%2C9%2C17%2C9H7C6.4%2C9%2C6.3%2C9.3%2C6.7%2C9.7L11.3%2C14.3z%22%2F%3E%3C%2Fsvg%3E');
      }
  

  
  </style>
  